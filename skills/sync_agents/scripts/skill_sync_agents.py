#!/home/jumasi/miniconda3/envs/goeq/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re

# 신규 이관된 .agents/ 하위의 agents/ 디렉터리 경로를 명확히 역산 (scripts -> sync_agents -> skills -> .agents/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
AGENT_DIR = os.path.join(ROOT_DIR, ".agents", "agents")

REGISTRY_PATH = os.path.join(AGENT_DIR, "agents_registry.json")
MANIFEST_PATH = os.path.join(AGENT_DIR, "agents.md")

# 통합 에이전트 협업 및 체이닝 다이어그램 (SSOT Mermaid)
INTEGRATED_MERMAID = """```mermaid
flowchart TD
    User["사용자 (Human User)"]
    Planner["Planner Orchestration Agent<br>[최상위 기획 에이전트]"]
    EDASubAgent["Data Insights Analyst<br>[사전 분석 서브에이전트]"]
    QueryPreBuilder["Data Layer Builder Agent<br>[쿼리/전처리 빌더 에이전트]"]
    DashboardLayerBuilder["Dashboard Layer Builder Agent<br>[화면/시각화 빌더 에이전트]"]
    PRD[".agents/context/prd/prd-*.md<br>(완성 및 확정된 PRD)"]
    
    %% 신규 추가된 리뷰 및 평가 체계
    CodeReviewer["Code Reviewer Agent<br>[리뷰어 서브에이전트]"]
    QualityEvaluator["Quality Evaluator Agent<br>[평가 서브에이전트]"]
    Gateway["최종 배포 게이트<br>(수동 병합 승인)"]

    User -->|"1. 개발 / 리팩토링 요구사항 전달"| Planner
    EDASubAgent -.->|"2. 사전 데이터 분석 리포트 제공"| Planner
    Planner <-->|"3. 초안 피드백 및 기획 소통"| User
    Planner -->|"4. 최종 PRD 확정 및 배포"| PRD

    PRD -->|"5. 데이터 가공 및 쿼리 구현 지침 제공"| QueryPreBuilder
    PRD -->|"6. 화면 및 차트 시각화 구성 지침 제공"| DashboardLayerBuilder

    QueryPreBuilder -->|"7. 서비스 모듈 데이터 공급"| DashboardLayerBuilder
    
    %% 리뷰 & 평가 파이프라인 체이닝
    DashboardLayerBuilder & QueryPreBuilder -->|"8. 코드 초안 제출"| CodeReviewer
    CodeReviewer -->|"9. 정적 피드백 & 리팩토링 가이드(Diff)"| QueryPreBuilder & DashboardLayerBuilder
    
    %% 스크립트 실행 동선과 가드레일 제어
    CodeReviewer -->|"10. 리뷰 정합성 검증 완료"| QualityEvaluator
    QualityEvaluator -->|"11. 하네스 테스트 & 린트/PRD 정량 평가"| QualityEvaluator
    
    QualityEvaluator -->|"12. Pass (평가 통과)"| Gateway
    QualityEvaluator -->|"12. Fail (재수정 요망)"| QueryPreBuilder & DashboardLayerBuilder
```"""


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["agents"]


def generate_manifest_table(agents):
    """JSON 데이터를 파싱하여 AGENT_MANIFEST.md 용 마크다운 표를 생성합니다."""
    table_lines = [
        "| Trigger | Agent | Required Context | Allowed Actions | Forbidden Actions | Verification | Output |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    # Planner -> Builder -> Sub-Agent 순서 보장
    ordered_keys = []
    # 1. Planner Agents
    ordered_keys.extend([k for k, v in agents.items() if v["category"] == "Planner Agent"])
    # 2. Builder Agents
    ordered_keys.extend([k for k, v in agents.items() if v["category"] == "Builder Agent"])
    # 3. Sub-Agents
    ordered_keys.extend([k for k, v in agents.items() if v["category"] == "Sub-Agent"])

    for k in agents.keys():
        if k not in ordered_keys:
            ordered_keys.append(k)

    for agent_id in ordered_keys:
        info = agents[agent_id]
        trigger = info["trigger"]
        name = f"`{agent_id}`<br>*({info['category']})*"
        contexts = "<br>".join([f"`{c}`" for c in info["contexts"]])
        allowed = "<br>".join([f"- {a}" for a in info["allowed"]])
        forbidden = "<br>".join([f"- {f}" for f in info["forbidden"]])
        output_str = "<br>".join([f"`{o}`" for o in info["outputs"]])

        verification_map = {
            "planner-orchestrator": "- `prd-template.md` 포맷 정합성 준수 검증<br>- 빌더들이 참조 가능한 3-Layer 매핑 설계 완성 여부 확인",
            "data-layer-builder": "- `make verify` 구문/린트 검사<br>- Pandas 예외처리 및 방어 연산 검증",
            "dashboard-layer-builder": "- 3-Layer 정합성 대조<br>- 차트 렌더링 검사<br>- 네비게이션 정상 등록 확인<br>- 미학적 디테일 및 이모지 검역",
            "data-insights-analyst": "- DDL/DML 쿼리 유무 검사 (Read-Only 여부)<br>- 보고서 산출물 내 결측치, 비즈니스 맥락 분석 유효성 대조",
            "governance-compliance-auditor": "- 명명 규정 위반 탐지 리포트 무결성<br>- 스키마-코드 1:1 컬럼 정합성 대조",
            "code-reviewer": "- 리뷰 리포트 규격 가독성 검토<br>- 제시한 리팩토링 가이드(Diff) 무결성 대조",
            "quality-evaluator": "- 테스트 구동 성공 신뢰도 검증<br>- 채점 매트릭 기반 정량 스코어 계산 무결성",
        }
        verification = verification_map.get(agent_id, "- 검증 기준 준증")

        row = f"| **{trigger}** | {name} | {contexts} | {allowed} | {forbidden} | {verification} | {output_str} |"
        table_lines.append(row)

    return "\n".join(table_lines)


def update_file_section(filepath, start_marker, end_marker, replacement_content):
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} not found.")
        return False

    content = ""
    encodings = ["utf-8", "cp949", "euc-kr"]
    loaded = False
    current_encoding = "utf-8"

    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            loaded = True
            current_encoding = enc
            break
        except Exception:
            continue

    if not loaded:
        print(f"Error: Could not decode file {filepath} with common encodings.")
        return False

    pattern = re.compile(rf"({re.escape(start_marker)}).*?({re.escape(end_marker)})", re.DOTALL)

    if not pattern.search(content):
        print(f"Warning: Markers {start_marker} not found in {os.path.basename(filepath)}.")
        return False

    new_content = pattern.sub(rf"\1\n{replacement_content}\n\2", content)

    with open(filepath, "w", encoding=current_encoding) as f:
        f.write(new_content)
    print(f"Successfully updated: {os.path.basename(filepath)} (encoding: {current_encoding})")
    return True


def main():
    if not os.path.exists(REGISTRY_PATH):
        print(f"Registry file not found at {REGISTRY_PATH}. Please create it first.")
        return

    agents = load_registry()
    manifest_table = generate_manifest_table(agents)

    # 1. AGENT_MANIFEST.md 내의 표(Table) 동기화
    update_file_section(MANIFEST_PATH, "<!-- START_AGENT_TABLE -->", "<!-- END_AGENT_TABLE -->", manifest_table)

    # 2. AGENT_MANIFEST.md 내의 다이어그램 동기화
    update_file_section(
        MANIFEST_PATH, "<!-- START_AGENT_CHAINING -->", "<!-- END_AGENT_CHAINING -->", INTEGRATED_MERMAID
    )

    # 3. 개별 에이전트 문서 내의 다이어그램 일괄 동기화
    for agent_id in agents.keys():
        doc_path = os.path.join(AGENT_DIR, "roles", f"{agent_id}.md")
        if os.path.exists(doc_path):
            update_file_section(
                doc_path, "<!-- START_AGENT_CHAINING -->", "<!-- END_AGENT_CHAINING -->", INTEGRATED_MERMAID
            )

    # 4. 개별 에이전트 폴더 및 agent.json 생성/동기화
    for agent_id, agent_info in agents.items():
        agent_folder = os.path.join(AGENT_DIR, agent_id)
        os.makedirs(agent_folder, exist_ok=True)
        agent_json_path = os.path.join(agent_folder, "agent.json")
        with open(agent_json_path, "w", encoding="utf-8") as f:
            json.dump(agent_info, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated: {agent_id}/agent.json")


if __name__ == "__main__":
    main()
