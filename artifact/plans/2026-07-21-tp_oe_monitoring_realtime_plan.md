# TP OE Monitoring Real-Time Data Source Transition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 리팩토링을 통해 `tp_oe_monitoring` 페이지의 품질 실적 데이터를 로컬 pre-aggregated SQLite 데이터(`staging.db`) 대신 실시간 Databricks 클라우드 데이터원천을 직접 쿼리하여 표출합니다.

**Architecture:** `staging.db`에서 5대 타깃 자재 메타 정보를 1차로 로드하고, Databricks에서 단일 통합 SQL을 수행하여 생산량, 스크랩, 리워크, 중량, Uniformity 실시간 실적을 일괄 수집(Left Join 결합) 및 dynamic KPI 계산(PPM, 합격률)을 실시간 처리합니다. Databricks 연결 차단 시 안전하게 0으로 실적을 채워 복원력을 제공하는 Robust Fallback을 수립합니다.

**Tech Stack:** Python 3.10+, Pandas, SQLite3, Databricks SQL, Streamlit

## Global Constraints
- **Constraint 1:** 일반 유니코드 이모지(⭐, ❗, ❌ 등)의 사용을 금지합니다. 아이콘이 필요한 경우 오직 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만을 사용해야 합니다.
- **Constraint 2:** `tests/` 디렉터리 하위 독립 테스트 작성을 통해서만 검증을 수행하고, 프로덕션 소스 코드 오염을 방지하기 위해 Mocking 및 인메모리 기법을 철저히 활용합니다.
- **Constraint 3:** 모든 AI 생성 아티팩트 및 계획 문서는 예외 없이 `.agents/artifact/` 디렉터리 하위에 생성하고 축적해야 합니다.

---

### Task 1: Refactor tp_oe_2026_service

**Files:**
- Modify: `app/service/tp_oe_2026_service.py`

**Interfaces:**
- Consumes: `get_client("databricks")` 및 `get_client("sqlite", sqlite_db_path="staging")`
- Produces: `get_tp_oe_2026_spec_data() -> pd.DataFrame`

- [ ] **Step 1: Write the service implementation**

Replace the whole file `app/service/tp_oe_2026_service.py` with the following implementation:

```python
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import sqlite3
from datetime import datetime
import pandas as pd
import logging
from app.core.infrastructure.db_client import get_client

logger = logging.getLogger(__name__)

# =========================================================================
# SECTION 2. Business Logic Service (비즈니스 쿼리 및 대상 선정 서비스)
# =========================================================================
def get_tp_oe_2026_spec_data() -> pd.DataFrame:
    """staging.db에서 2026년 이상 MP-GATE 및 TP 공장에 해당하는 타깃 규격 메타데이터를 수집하고,
    Databricks로부터 실시간 실적 데이터(생산량, Scrap, Rework, 중량, Uniformity)를 직접 조회하여 병합합니다.

    Returns
    -------
    pd.DataFrame
        실시간 데이터가 결합되고 PPM/합격률이 완벽히 연산된 데이터프레임
    """
    stg_path = "local.data/database/staging.db"
    
    # 1. SQLite staging.db에서 5대 타깃 마스터 규격 메타데이터 조회
    try:
        conn_stg = sqlite3.connect(stg_path)
        query_stg = """
            SELECT 
                MCODE,
                SPEC_CD,
                PLANT,
                MP_GATE_DT,
                MIN_WRK_DATE,
                [Supply Status],
                [Car Maker],
                [Vehicle Model Local]
            FROM iqm_plus_spec_master
            WHERE PLANT = 'TP' AND SUBSTR(MP_GATE_DT, 1, 4) >= '2026'
        """
        df_meta = pd.read_sql_query(query_stg, conn_stg)
        conn_stg.close()
    except Exception as e:
        logger.error(f"SQLite iqm_plus_spec_master 조회 오류: {str(e)}")
        return pd.DataFrame()

    if df_meta.empty:
        return pd.DataFrame()

    # 2. Databricks 실시간 실적 집계 통합 쿼리 정의
    query_dbx = """
    WITH spec_master AS (
        SELECT DISTINCT PLT_CD AS PLANT, PRD_CD AS MCODE, SPEC_CD
        FROM hkt_dw.specification.mas_d_lmastr101
        WHERE PLT_CD = 'TP' AND PRD_CD IN ('1033649', '1033647', '2022188', '1034831', '1034828')
    ),
    prod AS (
        SELECT PRD_CD AS MCODE, SUM(PRDT_QTY) AS PRDT_QTY
        FROM hkt_dw.production.wrk_f_lwrkts118
        WHERE PLT_CD = 'TP'
          AND PRD_CD IN ('1033649', '1033647', '2022188', '1034831', '1034828')
          AND WRK_DATE >= '20260101'
        GROUP BY PRD_CD
    ),
    ncf_proc AS (
        SELECT m.MCODE, ncf.INS_TP_CD, ncf.DFT_QTY
        FROM spec_master m
        INNER JOIN hkt_dw.quality.qlt_f_lqlttr107 ncf
           ON m.PLANT = ncf.PLT_CD AND m.SPEC_CD = ncf.SPEC_CD
        WHERE ncf.DFT_QTY > 0 AND ncf.INS_DATE >= '20260101'
    ),
    ncf_ship AS (
        SELECT m.MCODE, '1' AS INS_TP_CD, s.DFT_QTY
        FROM spec_master m
        INNER JOIN hkt_dw.quality.qlt_f_lqlttr120 s
           ON m.PLANT = s.PLT_CD AND m.SPEC_CD = s.SPEC_CD
        WHERE s.DFT_QTY > 0 AND s.INS_DATE >= '20260101' AND s.DFT_OCCR_FG = '1'
    ),
    ncf_all AS (
        SELECT MCODE, INS_TP_CD, DFT_QTY FROM ncf_proc
        UNION ALL
        SELECT MCODE, INS_TP_CD, DFT_QTY FROM ncf_ship
    ),
    ncf_agg AS (
        SELECT 
            MCODE,
            SUM(CASE WHEN INS_TP_CD IN ('1', '2', '3', '5') THEN DFT_QTY ELSE 0 END) AS SCRAP_DFT_QTY,
            SUM(CASE WHEN INS_TP_CD IN ('4', '6', '8', 'C', 'D', 'H', 'V') THEN DFT_QTY ELSE 0 END) AS REWORK_DFT_QTY
        FROM ncf_all
        GROUP BY MCODE
    ),
    wt AS (
        SELECT m.MCODE,
               CASE WHEN w.STD_WGT != 0 AND w.MRM_WGT >= (w.STD_WGT * 0.975) AND w.MRM_WGT <= (w.STD_WGT * 1.025) THEN 1 ELSE 0 END AS JDG
        FROM spec_master m
        INNER JOIN hkt_dw.quality.qlt_f_lqlttr127 w
           ON m.PLANT = w.PLT_CD AND m.SPEC_CD = w.SPEC_CD
        WHERE w.INS_DATE >= '20260101' AND w.MRM_WGT != 0
    ),
    wt_agg AS (
        SELECT 
            MCODE,
            COUNT(*) AS GT_WT_INS_COUNT,
            SUM(JDG) AS GT_WT_PASS_COUNT
        FROM wt
        GROUP BY MCODE
    ),
    uf AS (
        SELECT m.MCODE,
               CASE 
                   WHEN m.PLANT IN ('JP','HP','CP') AND u.JDG_GR <= 3 THEN 1
                   WHEN m.PLANT IN ('KP','DP','IP','MP','TP') AND u.JDG_GR <= 4 THEN 1
                   ELSE 0
               END AS JDG
        FROM spec_master m
        INNER JOIN hkt_quality.inspection.uniformity_result_raw u
           ON m.PLANT = u.PLT_CD AND m.SPEC_CD = u.SPEC_CD
        WHERE u.INS_DATE >= '20260101' AND u.INS_FG = '1'
    ),
    uf_agg AS (
        SELECT 
            MCODE,
            COUNT(*) AS UF_INS_COUNT,
            SUM(JDG) AS UF_PASS_COUNT
        FROM uf
        GROUP BY MCODE
    )
    SELECT 
        m.MCODE,
        COALESCE(p.PRDT_QTY, 0) AS PRDT_QTY,
        COALESCE(n.SCRAP_DFT_QTY, 0) AS SCRAP_DFT_QTY,
        COALESCE(n.REWORK_DFT_QTY, 0) AS REWORK_DFT_QTY,
        COALESCE(w.GT_WT_INS_COUNT, 0) AS GT_WT_INS_COUNT,
        COALESCE(w.GT_WT_PASS_COUNT, 0) AS GT_WT_PASS_COUNT,
        COALESCE(u.UF_INS_COUNT, 0) AS UF_INS_COUNT,
        COALESCE(u.UF_PASS_COUNT, 0) AS UF_PASS_COUNT
    FROM (SELECT DISTINCT MCODE FROM spec_master) m
    LEFT JOIN prod p ON m.MCODE = p.MCODE
    LEFT JOIN ncf_agg n ON m.MCODE = n.MCODE
    LEFT JOIN wt_agg w ON m.MCODE = w.MCODE
    LEFT JOIN uf_agg u ON m.MCODE = u.MCODE
    """

    # 3. Databricks 쿼리 실행 및 Robust Fallback 가동
    df_perf = None
    try:
        dbx_client = get_client("databricks")
        df_perf = dbx_client.execute(query_dbx)
        if df_perf is not None and not df_perf.empty:
            df_perf.columns = [col.upper() for col in df_perf.columns]
            df_perf["MCODE"] = df_perf["MCODE"].astype(str).str.strip()
    except Exception as e:
        logger.warning(f"Databricks 실시간 조회 실패 (안전 Fallback 가동): {str(e)}")
        df_perf = pd.DataFrame()

    # 4. 성능 실적이 비어있는 경우(또는 에러 시)를 위한 Zero-Filled 기본 프레임 생성
    if df_perf is None or df_perf.empty:
        df_perf = pd.DataFrame(columns=[
            "MCODE", "PRDT_QTY", "SCRAP_DFT_QTY", "REWORK_DFT_QTY", 
            "GT_WT_INS_COUNT", "GT_WT_PASS_COUNT", "UF_INS_COUNT", "UF_PASS_COUNT"
        ])

    # 5. 메타데이터 데이터프레임과 성능 실적 Left Join 결합
    df_meta["MCODE"] = df_meta["MCODE"].astype(str).str.strip()
    df_combined = pd.merge(df_meta, df_perf, on="MCODE", how="left")

    # NaN 값 0 채우기
    metric_cols = [
        "PRDT_QTY", "SCRAP_DFT_QTY", "REWORK_DFT_QTY", 
        "GT_WT_INS_COUNT", "GT_WT_PASS_COUNT", "UF_INS_COUNT", "UF_PASS_COUNT"
    ]
    for col in metric_cols:
        df_combined[col] = pd.to_numeric(df_combined[col], errors="coerce").fillna(0.0)

    # 6. 양산 경과일 (MASS_PERIOD) 실시간 동적 계산
    def calculate_mass_period(row):
        val = row["MIN_WRK_DATE"]
        if not val or pd.isna(val) or str(val).strip() in ["", "-", "None"]:
            return 0
        try:
            val_str = str(val).replace("-", "").strip()
            if len(val_str) == 8:
                start_dt = datetime.strptime(val_str, "%Y%m%d")
                days_diff = (datetime.now() - start_dt).days
                return max(0, days_diff)
        except Exception:
            pass
        return 0

    df_combined["MASS_PERIOD"] = df_combined.apply(calculate_mass_period, axis=1)

    # -------------------------------------------------------------------------
    # 결측치 문자열 및 날짜 YYYY-MM-DD 형식 처리
    # -------------------------------------------------------------------------
    def format_date_to_hyphen(val):
        if not val or pd.isna(val) or str(val).strip() in ["", "-", "None"]:
            return "-"
        val_str = str(val).replace("-", "").strip()
        if len(val_str) == 8:
            return f"{val_str[:4]}-{val_str[4:6]}-{val_str[6:]}"
        return val_str

    df_combined["SPEC_CD"] = df_combined["SPEC_CD"].fillna("-").replace("", "-")
    df_combined["MIN_WRK_DATE"] = df_combined["MIN_WRK_DATE"].apply(format_date_to_hyphen)
    df_combined["MP_GATE_DT"] = df_combined["MP_GATE_DT"].apply(format_date_to_hyphen)

    # -------------------------------------------------------------------------
    # 파생 변수 (PPM, 합격률) 실시간 계산
    # -------------------------------------------------------------------------
    df_combined["SCRAP_PPM"] = df_combined.apply(
        lambda r: round((r["SCRAP_DFT_QTY"] / r["PRDT_QTY"] * 1000000), 1) if r["PRDT_QTY"] > 0 else 0.0,
        axis=1
    )
    df_combined["REWORK_PPM"] = df_combined.apply(
        lambda r: round((r["REWORK_DFT_QTY"] / r["PRDT_QTY"] * 1000000), 1) if r["PRDT_QTY"] > 0 else 0.0,
        axis=1
    )
    df_combined["GT_WT_PASS_RATE"] = df_combined.apply(
        lambda r: round((r["GT_WT_PASS_COUNT"] / r["GT_WT_INS_COUNT"] * 100), 2) if r["GT_WT_INS_COUNT"] > 0 else 0.0,
        axis=1
    )
    df_combined["UF_PASS_RATE"] = df_combined.apply(
        lambda r: round((r["UF_PASS_COUNT"] / r["UF_INS_COUNT"] * 100), 2) if r["UF_INS_COUNT"] > 0 else 0.0,
        axis=1
    )

    return df_combined
```

---

### Task 2: Implement Unit and Mock Tests

**Files:**
- Modify: `tests/test_tp_oe_2026_service.py`

**Interfaces:**
- Consumes: `get_tp_oe_2026_spec_data`
- Produces: `None` (pytest execution)

- [ ] **Step 1: Write test cases covering both success (real-time) and fallback scenarios**

Overwrite the contents of `tests/test_tp_oe_2026_service.py` with:

```python
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import pandas as pd
from unittest.mock import patch, MagicMock
from app.service.tp_oe_2026_service import get_tp_oe_2026_spec_data


# =========================================================================
# SECTION 2. Test Cases (단위 테스트 케이스 정의)
# =========================================================================
def test_get_tp_oe_2026_spec_data_golden_path() -> None:
    """Databricks 원천 데이터가 있을 때 정상 수집 및 KPI 연산이 정상 수행되는지 검증합니다."""
    # Mock Databricks Client 생성
    mock_perf_df = pd.DataFrame([
        {
            "MCODE": "1033649", "PRDT_QTY": 5000.0, "SCRAP_DFT_QTY": 10.0, "REWORK_DFT_QTY": 50.0,
            "GT_WT_INS_COUNT": 100, "GT_WT_PASS_COUNT": 98, "UF_INS_COUNT": 100, "UF_PASS_COUNT": 95
        },
        {
            "MCODE": "1033647", "PRDT_QTY": 1000.0, "SCRAP_DFT_QTY": 5.0, "REWORK_DFT_QTY": 20.0,
            "GT_WT_INS_COUNT": 50, "GT_WT_PASS_COUNT": 50, "UF_INS_COUNT": 50, "UF_PASS_COUNT": 45
        }
    ])

    with patch("app.service.tp_oe_2026_service.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.execute.return_value = mock_perf_df
        mock_get_client.return_value = mock_client

        df = get_tp_oe_2026_spec_data()

        # 형식 검증
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

        # 특정 타깃 MCODE 추출 후 연산값 검증 (1033649)
        row_1033649 = df[df["MCODE"] == "1033649"].iloc[0]
        assert row_1033649["PRDT_QTY"] == 5000.0
        assert row_1033649["SCRAP_PPM"] == 2000.0  # 10 / 5000 * 1,000,000
        assert row_1033649["REWORK_PPM"] == 10000.0 # 50 / 5000 * 1,000,000
        assert row_1033649["GT_WT_PASS_RATE"] == 98.0
        assert row_1033649["UF_PASS_RATE"] == 95.0


def test_get_tp_oe_2026_spec_data_fallback() -> None:
    """Databricks 연결 오류 발생 시에도 안전하게 Robust Fallback이 가동되어 0으로 채워진 데이터가 정상 반환되는지 검증합니다."""
    with patch("app.service.tp_oe_2026_service.get_client", side_effect=Exception("Connection Failed")):
        df = get_tp_oe_2026_spec_data()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty

        # 5대 타깃 자재가 모두 안전하게 로드되었는지 확인
        expected_mcodes = {"1033649", "1033647", "2022188", "1034831", "1034828"}
        actual_mcodes = set(df["MCODE"].astype(str).str.strip().tolist())
        assert expected_mcodes.issubset(actual_mcodes)

        # 실적이 에러로 인해 0 또는 기본값으로 잘 바인딩되었는지 확인 (1034831)
        row_1034831 = df[df["MCODE"] == "1034831"].iloc[0]
        assert row_1034831["PRDT_QTY"] == 0.0
        assert row_1034831["SCRAP_DFT_QTY"] == 0.0
        assert row_1034831["SCRAP_PPM"] == 0.0
        assert row_1034831["GT_WT_PASS_RATE"] == 0.0
```

- [ ] **Step 2: Run pytest to verify all test cases pass**

Run: `pytest tests/test_tp_oe_2026_service.py -v`
Expected: 2 passed

- [ ] **Step 3: Commit**

```bash
git add app/service/tp_oe_2026_service.py tests/test_tp_oe_2026_service.py
git commit -m "feat: refactor tp_oe_2026_service to query Databricks in real-time with robust fallback"
```

---

### Task 3: Update Documentation (prd_tp_oe_monitoring.md)

**Files:**
- Modify: `app/pages/_10_dashboard/tp_oe_monitoring/prd_tp_oe_monitoring.md`

- [ ] **Step 1: Update data sources details inside prd_tp_oe_monitoring.md**

Modify the file `app/pages/_10_dashboard/tp_oe_monitoring/prd_tp_oe_monitoring.md`:
In `SECTION 1. DATA SOURCES & USED FIELDS` and `SECTION 4. BUSINESS LOGIC & CALCULATION FORMULAS`, update references to stop using the pre-aggregated `tp_oe_2026_target_metrics_agg` view, and document the live Databricks querying and fallback mechanism.

- [ ] **Step 2: Commit**

```bash
git add app/pages/_10_dashboard/tp_oe_monitoring/prd_tp_oe_monitoring.md
git commit -m "docs: update prd_tp_oe_monitoring.md data source documentation"
```
