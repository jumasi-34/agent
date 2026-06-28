---
id: skill.understand.domain
type: reference
status: active

summary: >
  Domain 참조 및 가이드 명세서.

parent: "[[skills/understand/SKILL]]"

updated: 2026-06-28---
# 비즈니스 도메인 지식 흐름 추출 가이드라인 (understand-domain)

* **Parent (상위 스킬)**: [SKILL.md](../SKILL.md)

---


본 지침은 코드베이스 내에 축적된 비즈니스 도메인 지식(도메인 영역, 비즈니스 흐름 및 세부 처리 단계)을 식별하고 추출하여 대시보드상에 수평적 도메인 플로우 그래프를 가시화하기 위한 분석 가이드라인입니다.

## 기본 작동 원리 (How It Works)

- **지식 그래프 활용**: 이미 지식 그래프(`.understand-anything/knowledge-graph.json`)가 워크스페이스 내에 존재한다면, 소스 파일을 하나씩 새로 검색하는 비용을 줄이고 지식 그래프 데이터로부터 도메인 지식을 유추 및 추출합니다.
- **경량 스캔(Lightweight Scan)**: 기존 지식 그래프가 없을 경우, 파일 트리 및 엔트리 포인트 감지, 그리고 샘플링된 파일을 기반으로 경량 정적 가인덱싱을 우선 수행합니다.
- **전수 재생성 제어**: `--full` 플래그가 주입될 경우, 기존 지식 그래프의 존재 여부와 상관없이 무조건 처음부터 전체 스캔을 강제합니다.

## 세부 단계별 구동 지침 (Instructions)

### 단계 0: 프로젝트 루트 경로 분석 및 조정 (Resolve PROJECT_ROOT)

1.  `PROJECT_ROOT`를 현재 작업 디렉토리(CWD)로 설정하십시오.
2.  **Git Worktree 분기 감지 및 우회 처리**: 만약 `PROJECT_ROOT`가 일시적이고 가상적인 Git Worktree 내부를 가리키고 있다면, 최종 마크다운 및 그래프 자산 유실을 원천 방지하기 위해 물리 메인 저장소(Main repository)의 루트 경로로 출력 위치를 조정해야 합니다.
    - 아래 Bash 스크립트를 기동하여 메인 저장소 루트 경로를 식별 및 조정하십시오.
      ```bash
      COMMON_DIR=$(git -C "$PROJECT_ROOT" rev-parse --git-common-dir 2>/dev/null)
      GIT_DIR=$(git -C "$PROJECT_ROOT" rev-parse --git-dir 2>/dev/null)
      if [ -n "$COMMON_DIR" ] && [ -n "$GIT_DIR" ]; then
        COMMON_ABS=$(cd "$PROJECT_ROOT" && cd "$COMMON_DIR" 2>/dev/null && pwd -P)
        GIT_ABS=$(cd "$PROJECT_ROOT" && cd "$GIT_DIR" 2>/dev/null && pwd -P)
        if [ -n "$COMMON_ABS" ] && [ "$COMMON_ABS" != "$GIT_ABS" ]; then
          MAIN_ROOT=$(dirname "$COMMON_ABS")
          if [ -d "$MAIN_ROOT" ] && [ "${UNDERSTAND_NO_WORKTREE_REDIRECT:-0}" != "1" ]; then
            echo "[understand-domain] Detected git worktree at $PROJECT_ROOT"
            echo "[understand-domain] Redirecting output to main repo root: $MAIN_ROOT"
            echo "[understand-domain] (Set UNDERSTAND_NO_WORKTREE_REDIRECT=1 to keep PROJECT_ROOT as the worktree.)"
            PROJECT_ROOT="$MAIN_ROOT"
          fi
        fi
      fi
      ```
    - 이후 모든 가이드 단계에서 타겟 프로젝트 폴더를 탐색할 때는 설정된 `$PROJECT_ROOT` 변수를 엄격히 적용하십시오.
3.  **플러그인 루트 식별**: 플러그인의 절대 기준 경로(`PLUGIN_ROOT`)를 파악하기 위해 아래의 후보군을 순차 점검하십시오.
    ```bash
    SKILL_REAL=$(realpath ~/.agents/skills/understand-domain 2>/dev/null || readlink -f ~/.agents/skills/understand-domain 2>/dev/null || echo "")
    SELF_RELATIVE=$([ -n "$SKILL_REAL" ] && cd "$SKILL_REAL/../.." 2>/dev/null && pwd || echo "")
    COPILOT_SKILL_REAL=$(realpath ~/.copilot/skills/understand-domain 2>/dev/null || readlink -f ~/.copilot/skills/understand-domain 2>/dev/null || echo "")
    COPILOT_SELF_RELATIVE=$([ -n "$COPILOT_SKILL_REAL" ] && cd "$COPILOT_SKILL_REAL/../.." 2>/dev/null && pwd || echo "")

    PLUGIN_ROOT=""
    for candidate in \
      "${CLAUDE_PLUGIN_ROOT}" \
      "$HOME/.understand-anything-plugin" \
      "$SELF_RELATIVE" \
      "$COPILOT_SELF_RELATIVE" \
      "$HOME/.codex/understand-anything/understand-anything-plugin" \
      "$HOME/.opencode/understand-anything/understand-anything-plugin" \
      "$HOME/.pi/understand-anything/understand-anything-plugin" \
      "$HOME/understand-anything/understand-anything-plugin"; do
      if [ -n "$candidate" ] && [ -f "$candidate/package.json" ] && [ -f "$candidate/pnpm-workspace.yaml" ]; then
        PLUGIN_ROOT="$candidate"
        break
      fi
    done
    ```

### 단계 1: 기존 지식 그래프 탐색 (Detect Existing Graph)

1.  `$PROJECT_ROOT/.understand-anything/knowledge-graph.json` 파일이 존재하는지 검증하십시오.
2.  해당 파일이 존재하고 `--full` 옵션이 주입되지 않았다면 **단계 3(기존 그래프 파생 경로)**으로 직접 건너뛰십시오.
3.  그렇지 않은 경우 **단계 2(경량 코드 스캔 경로)**를 개시합니다.

### 단계 2: 경량 코드 스캔 수행 (Lightweight Scan)

이 단계에서는 고가의 LLM 자원을 직접 기동하기 전, 저비용의 파이썬 전처리 스크립트를 돌려 도메인 텍스트 분석에 필요한 원천 구조 컨텍스트(파일 트리, 엔트리 포인트, 임포트 구조 등)를 선행 획득합니다.
1.  동봉된 파이썬 스크립트를 기동하여 임시 가분석 메타데이터를 저장하십시오.
    ```bash
    python ./extract-domain-context.py "$PROJECT_ROOT"
    ```
2.  실행이 완료되면 생성된 `$PROJECT_ROOT/.understand-anything/intermediate/domain-context.json` 데이터를 로드하고 **단계 4**로 진입합니다.

### 단계 3: 기존 그래프 정보 가공 (Derive from Existing Graph)

1.  이미 빌드되어 있는 `$PROJECT_ROOT/.understand-anything/knowledge-graph.json` 데이터를 정독하십시오.
2.  노드 유형, 모듈 설명, `contains`/`calls` 등 구조적 연관 관계 정보를 분석 모델(LLM)에 전달할 경량 정제 텍스트 포맷으로 가공합니다.
3.  가공 완료 후 해당 컨텍스트 정보를 품고 **단계 4**로 진입합니다.

### 단계 4: 도메인 분석 실행 (Domain Analysis)

1.  에이전트 제어 프롬프트 지침서가 기재된 `$PLUGIN_ROOT/agents/domain-analyzer.md` 파일 내용을 로드하십시오.
2.  자격 요건을 갖춘 서브에이전트(Subagent)를 기동하고, 단계 2 혹은 단계 3에서 추출해낸 구조 메타데이터를 분석 주입 컨텍스트로 전달하여 심층 도메인 모델링을 위임하십시오.
3.  에이전트는 결과물인 비즈니스 도메인 모델 JSON 데이터를 `$PROJECT_ROOT/.understand-anything/intermediate/domain-analysis.json`에 임시 저장합니다.

### 단계 5: 유효성 검증 및 데이터 저장 (Validate and Save)

1.  생성된 비즈니스 분석 JSON 파일의 스키마 구조를 탐색하십시오. (도메인, 도메인 플로우, 단계 노드 등)
2.  표준 그래프 유효성 검증 규칙(Validation pipeline)을 기동하고, 관계 고리 중 끊어진 엣지나 불완전한 노드가 발견될 경우 정비하거나 안전하게 보정하십시오.
3.  최종 정제된 데이터를 `$PROJECT_ROOT/.understand-anything/domain-graph.json` 경로에 배포 저장하십시오.
4.  임시 중간 데이터들이 저장되었던 `intermediate` 하위의 파일들은 깔끔하게 소거하십시오.

### 단계 6: 대시보드 연동 기동 (Launch Dashboard)

1.  비즈니스 도메인 그래프 분석 결과를 즉각 브라우저에서 관측할 수 있도록 `/understand-dashboard` 스킬을 자동 호출 구동하십시오.
2.  해당 대시보드는 폴더 내의 `domain-graph.json`을 자동 인지하여 메인 도메인 수평 흐름 차트를 브라우저에 표시하게 됩니다.
