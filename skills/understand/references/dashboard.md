---
id: skill.understand.dashboard
type: reference
status: active

summary: >
  Dashboard 참조 및 가이드 명세서.

parent: "[[skills/understand/SKILL.md]]"

updated: 2026-06-28
---

# 지식 그래프 시각화 대시보드 가이드라인 (understand-dashboard)

* **Parent (상위 스킬)**: [[skills/understand/SKILL.md]]

---


본 지침은 생성된 지식 그래프를 시각적으로 탐색하기 위해 대시보드 웹 인터페이스를 구동하고 올바르게 연동하는 제어 가이드라인입니다.

## 세부 구동 및 연동 지침 (Instructions)

1.  **대상 프로젝트 디렉토리 식별**:
    - 전달된 인자(`$ARGUMENTS`)에 분석 대상 경로가 포함되어 있다면 해당 경로를 사용하십시오.
    - 경로가 없다면 현재 작업 디렉토리(Current Working Directory)를 프로젝트 디렉토리로 간주합니다.

2.  **지식 그래프 존재 여부 확인**:
    - 대상 프로젝트 디렉토리 하위에 `.understand-anything/knowledge-graph.json`이 존재하는지 확인하십시오.
    - 파일이 발견되지 않을 경우 아래와 같은 경고 메시지를 사용자에게 보여주고 가이드를 중단하십시오.
      ```
      No knowledge graph found. Run /understand first to analyze this project.
      ```

3.  **대시보드 패키지 경로 탐색**:
    - 대시보드의 소스코드는 플러그인 루트 디렉토리 기준의 `packages/dashboard/` 하위에 위치합니다. 아래의 후보 경로들을 순차적으로 검증하여 가장 먼저 존재하는 유효한 디렉토리를 찾아내십시오.
      - `${CLAUDE_PLUGIN_ROOT}/packages/dashboard/` (가장 높은 우선순위)
      - `~/.understand-anything-plugin/packages/dashboard/` (공통 심볼릭 링크)
      - 현 스킬 기준의 상대 경로 상위 2단계 (`~/.agents/skills/understand-dashboard`의 실물 경로 기준)
      - 깃 클론 기반의 다양한 설치 예상 경로:
        - `~/.codex/understand-anything/understand-anything-plugin/packages/dashboard/`
        - `~/.opencode/understand-anything/understand-anything-plugin/packages/dashboard/`
        - `~/.pi/understand-anything/understand-anything-plugin/packages/dashboard/`
        - `~/understand-anything/understand-anything-plugin/packages/dashboard/`
    - 아래 Bash 스크립트 블록을 기동하여 실물 플러그인 루트(`PLUGIN_ROOT`)를 파악하십시오.
      ```bash
      SKILL_REAL=$(realpath ~/.agents/skills/understand-dashboard 2>/dev/null || readlink -f ~/.agents/skills/understand-dashboard 2>/dev/null || echo "")
      SELF_RELATIVE=$([ -n "$SKILL_REAL" ] && cd "$SKILL_REAL/../.." 2>/dev/null && pwd || echo "")
      COPILOT_SKILL_REAL=$(realpath ~/.copilot/skills/understand-dashboard 2>/dev/null || readlink -f ~/.copilot/skills/understand-dashboard 2>/dev/null || echo "")
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
        if [ -n "$candidate" ] && [ -d "$candidate/packages/dashboard" ]; then
          PLUGIN_ROOT="$candidate"; break
        fi
      done
      ```

4.  **의존성 설치 및 빌드**:
    - 대시보드 디렉토리로 이동하여 필요한 npm 패키지들을 설치하십시오.
      ```bash
      cd <dashboard-dir> && pnpm install --frozen-lockfile 2>/dev/null || pnpm install
      ```
    - 그 후 대시보드가 의존하는 핵심 코어 패키지를 빌드하십시오.
      ```bash
      cd <plugin-root> && pnpm --filter @understand-anything/core build
      ```

5.  **Vite 개발 서버 기동**:
    - 분석 대상 프로젝트의 지식 그래프 방향을 가리키는 환경 변수를 주입하여 Vite 개발 서버를 기동하십시오.
      ```bash
      cd <dashboard-dir> && GRAPH_DIR=<project-dir> npx vite --host 127.0.0.1
      ```
    - 사용자가 지속적으로 작업할 수 있도록 이 명령은 **백그라운드 태스크**로 실행해야 합니다.

6.  **액세스 인증 토큰(Access Token) 주소 캡처**:
    - Vite 서버 구동 시 터미널 출력에서 인증 토큰 매개변수가 포함된 대시보드 URL 주소 라인을 캡처하십시오. 출력 예시는 다음과 같습니다.
      ```
      Dashboard URL: http://127.0.0.1:<PORT>?token=<TOKEN>
      ```
    - 이 `?token=` 매개변수가 생략될 경우 대시보드 화면 진입 시 "Access Token Required" 차단 막이 활성화되므로, **반드시 토큰이 결합된 전체 주소**를 사용자에게 보고해야 합니다.

7.  **기동 완료 및 안내 보고**:
    - 기동 완료 후 아래 양식과 같이 전체 토큰 주소 및 대상 지식 그래프 위치를 한글로 간결하고 친절하게 보고하십시오.
      ```
      대시보드가 백그라운드에서 실행되었습니다: http://127.0.0.1:<PORT>?token=<TOKEN>
      대상 지식 그래프: <project-dir>/.understand-anything/knowledge-graph.json

      대시보드는 백그라운드에서 동작 중입니다. 터미널에서 Ctrl+C를 입력하면 구동을 중단할 수 있습니다.
      ```

## 운영 고려사항 (Notes)

- 대시보드는 `--open` 플래그를 통해 기본 웹 브라우저에서 자동으로 오픈되도록 구성할 수 있습니다.
- 만약 5173 포트가 이미 점유되어 있다면 Vite가 사용 가능한 다음 포트를 자동 감지하여 할당합니다.
- `GRAPH_DIR` 환경 변수를 정교하게 주입해야 대시보드 내에서 원천 데이터를 올바르게 읽어들입니다.
