# MagicSquare (4×4)

부분적으로 채워진 **4×4** 격자에서 빈칸 **2개**와 누락 숫자 **2개**를 고정 규칙으로 배치해, 모든 행·열·두 주 대각선의 합이 **Magic Constant 34**가 되도록 하는 **완성 결과**를 반환하는 Python 학습 프로젝트입니다. 그래픽 UI·DB 없이 **동일 요구사항**을 테스트와 경계 계약으로 검증하는 것을 목표로 합니다.

**문서 관계(한 줄):** `Report/1`~`Report/4`와 `.cursorrules`를 바탕으로 한 요구사항이 **`docs/PRD_MagicSquare_4x4_TDD.md`**에 구조화되어 확정되었고, 본 README의 본문·To-Do·검증 기준은 그 PRD를 중심 축으로 합니다. 상세 정렬 절차는 [`Report/5.prd_authoring_and_document_export.md`](Report/5.prd_authoring_and_document_export.md)를 참고하세요.

---

## 문서 맵

| 문서 | 역할 |
|------|------|
| [`docs/PRD_MagicSquare_4x4_TDD.md`](docs/PRD_MagicSquare_4x4_TDD.md) | **단일 출처:** FR·AC·범위·Dual-Track·NFR·시드·추적 매트릭스 |
| [`Report/4.user_journey_epic_to_technical_scenario.md`](Report/4.user_journey_epic_to_technical_scenario.md) | Epic·여정·User Story·Gherkin 표현 |
| [`Report/2.4x4_magic_square_dual_track_tdd_design.md`](Report/2.4x4_magic_square_dual_track_tdd_design.md) | INV·계약·오류 코드·U-/D- 테스트 ID 요약 |
| [`Report/3.cursorrules_specification_and_ai_guidelines.md`](Report/3.cursorrules_specification_and_ai_guidelines.md) | `.cursorrules` 요지(ECB·TDD·pytest) |
| [`.cursorrules`](.cursorrules) | 저장소 개발 규칙(실행·레이어·금지 사항) |
| [`Report/6.readme_backlog_and_environment_report.md`](Report/6.readme_backlog_and_environment_report.md) | README·구현 백로그·venv·TDD 보강 작업 보고 |
| [`Report/7.virtual_environment_and_pytest_execution.md`](Report/7.virtual_environment_and_pytest_execution.md) | 가상환경 활성화부터 `pytest` 실행까지 순서 요약 |

---

## 범위 요약 (PRD)

| 구분 | 내용 |
|------|------|
| **In** | 빈칸 좌표(row-major)·누락 숫자 2개·마방진 판정·두 고정 배치 시도·경계 입력 검증 |
| **Out** | 그래픽 UI, DB 필수, N×N 일반화(기본), 빈 격자에서의 완전 생성 솔버 |

---

## User Story (Report/4 정렬)

| ID | 제목 | 핵심 검증 |
|----|------|-----------|
| US-1 | 입력 검증 | 4×4, 빈칸 2, 무중복, 범위 1~16 |
| US-2 | 빈칸 탐색 | row-major, 좌표 2개(1-index) |
| US-3 | 누락 숫자 | 1~16 중 2개, `(n_small ≤ n_large)` |
| US-4 | 마방진 판정 | 행·열·두 대각선 합 34 |
| US-5 | 두 조합 시도 | 작은 수→첫 빈칸 우선, 실패 시 순서 반대, 성공 시 `int[6]` |

---

## 입출력·오류 계약 요약 (Report/2 / PRD §8.1)

**입력:** `int[][]` 논리 4×4 · `0` = 빈칸 **정확히 2개** · 셀은 `0` 또는 `1`~`16` · `0` 제외 중복 없음 · 첫 빈칸은 **row-major** 최초 `0`.

**출력(성공):** `int[6]` = `[r1, c1, n1, r2, c2, n2]` (좌표 **1-index**).

**시도:** 시도 1 = 작은 누락 수→첫 빈칸, 큰 수→둘째 빈칸 → 마방진이면 그 순서로 반환. 아니면 시도 2(순서 반대). 둘 다 실패 시 아래 `E_DOMAIN`.

| code | 조건(요약) | message (PRD와 문자 단위 일치) |
|------|------------|-------------------------------|
| `E_SIZE` | 행/열 수 ≠ 4 | `Grid must be 4 by 4.` |
| `E_EMPTY_COUNT` | `0` 개수 ≠ 2 | `There must be exactly two empty cells (value 0).` |
| `E_VALUE_RANGE` | 0 및 1~16 외 값 | `Each cell must be 0 or an integer from 1 to 16.` |
| `E_DUPLICATE` | 0 제외 중복 | `Values from 1 to 16 must not repeat except for 0.` |
| `E_DOMAIN` | 입력은 유효하나 두 시도 모두 비마방진 | `No valid magic square completion exists for this grid.` |

---

## 아키텍처 (Report/3 + `.cursorrules`)

- **패턴:** ECB(Entity–Control–Boundary). 의존성: **boundary → control → entity** (역방향 금지).
- **boundary:** 입출력·검증·CLI 등 외부 접점. 도메인 규칙을 직접 구현하지 않음.
- **control:** 검증 통과 후 도메인 유스케이스 조율(규칙 복제 없음).
- **entity:** 격자·불변조건·순수 판정·두 시도 로직(I/O 없음).
- **언어 / 테스트:** Python **3.10+**, **pytest**, Arrange–Act–Assert, 테스트 파일·함수는 `test_` 접두사.

권장 패키지 레이아웃은 [`.cursorrules`](.cursorrules)의 `file_structure`를 따릅니다.

---

## 개발 환경 설정 (가상 환경 기본)

이 저장소에서는 **시스템 전역 Python에 의존하지 않고**, 프로젝트 루트의 **로컬 가상 환경**에서 작업하는 것을 기본으로 합니다.

### 사전 요구

| 항목 | 버전·비고 |
|------|-----------|
| Python | **3.10 이상** (`.cursorrules`의 `code_style.python_version`) |
| pip | 가상 환경 생성 후 최신으로 올리는 것을 권장 |

설치 확인:

```bash
python --version
```

Windows에서 `python`이 없으면 Microsoft Store 또는 [python.org](https://www.python.org/downloads/) 설치 후, **“Add Python to PATH”** 옵션을 켜 두는 것이 좋습니다.

### 1. 가상 환경 만들기

저장소 루트(`MagicSquare_08` 등)에서:

```bash
python -m venv .venv
```

- 가상 환경 디렉터리 이름은 **`.venv`**를 권장합니다. `.gitignore`에 `.venv/`를 넣어 버전 관리에서 제외하는 것이 일반적입니다.
- 다른 이름을 쓰어도 되지만, 문서·팀 내에서 하나로 통일하는 것이 좋습니다.

### 2. 가상 환경 활성화

**Windows — PowerShell (기본 터미널)**

```powershell
.\.venv\Scripts\Activate.ps1
```

실행 정책 오류가 나면 *현재 사용자* 범위에서만 허용 예시:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows — 명령 프롬프트(cmd)**

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux (bash 등)**

```bash
source .venv/bin/activate
```

프롬프트 앞에 `(.venv)` 같이 표시되면 활성화된 상태입니다.

### 3. pip 업그레이드 및 의존성 설치

가상 환경이 **켜진 상태**에서:

```bash
python -m pip install --upgrade pip
```

테스트 실행을 위해 최소한 다음을 설치합니다.

```bash
pip install pytest pytest-cov
```

- **`pytest`**: 단위·통합 테스트 (`testing.framework` — `.cursorrules`).
- **`pytest-cov`**: 커버리지 리포트(PRD **§7** NFR-01·NFR-02 측정에 사용).

저장소에 **`pyproject.toml`** 또는 **`requirements.txt`** / **`requirements-dev.txt`**가 추가되면, 아래처럼 한 번에 설치하는 방식으로 바꿉니다.

```bash
pip install -r requirements-dev.txt
# 또는
pip install -e ".[dev]"
```

(`pyproject.toml` 내용에 맞게 조정)

### 4. 테스트 실행

가상 환경 **활성화 후**:

```bash
python -m pytest
```

커버리지까지 보려면(패키지 경로는 구현 후 `magic_square` 등 실제 모듈명에 맞게 조정):

```bash
python -m pytest --cov=magic_square --cov-report=term-missing
```

- `.cursorrules`의 **`testing.coverage_minimum`**(예: **80%**)은 저장소 전체 기준 하한으로 두는 경우가 많습니다.
- PRD **§7**은 추가로 **도메인 로직 ≥ 95%**, **경계 검증·매핑 ≥ 85%**를 요구하므로, 패키지를 나눈 뒤에는 `--cov` 대상을 entity / boundary 모듈별로 나누어 확인하는 것을 권장합니다.

### 5. 작업 종료 시

가상 환경 비활성화:

```bash
deactivate
```

다음 작업 때 다시 `Activate`만 하면 됩니다.

### IDE / Cursor

- Python 인터프리터 경로를 **`.venv\Scripts\python.exe`** (Windows) 또는 **`.venv/bin/python`** (Unix)로 지정하면, 터미널과 동일한 환경에서 테스트·디버깅이 맞습니다.

---

## TDD 사이클과 리팩터링

PRD **§8 Dual-Track TDD**와 [`.cursorrules`](.cursorrules)의 **`tdd_rules`**를 함께 적용합니다.

### RED → GREEN → REFACTOR

| 단계 | 하는 일 | 금지·주의 (`.cursorrules` 요지) |
|------|---------|--------------------------------|
| **RED** | 실패하는 테스트를 먼저 추가해 요구사항을 실행 가능한 스펙으로 고정한다. | RED 확인 없이 프로덕션 코드만 먼저 작성하지 않는다. |
| **GREEN** | 테스트를 통과하는 **가장 단순한** 구현만 추가한다. ECB 레이어 위치를 지킨다. | 이 단계에서 구조 개선·이름 변경 등 **리팩터링을 하지 않는다**. |
| **REFACTOR** | 동작은 유지한 채 읽기 좋은 구조로 정리한다. | 새 기능·버그 수정과 **한 커밋에 섞지 않는다**. 테스트는 전부 통과한 상태에서만 수행한다. |

### 리팩터링 시 유지할 것

- **커버리지**: 리팩터링 후에도 `testing.coverage_minimum` **미만으로 떨어지지 않게** 유지한다.
- **의존성 방향**: boundary → control → entity만 허용한다.
- **Dual-Track**: PRD §8.3 — 한 트랙만 끝내고 나머지를 나중에 몰아서 하지 말고, **경계와 도메인을 같은 주기**에서 번갈아 최소 통과를 유지한다.

리팩터링은 “테스트가 녹색일 때만”“기능 변경 없이” 수행한다는 점이 PRD의 훈련 목표와 직결됩니다.

### Git 브랜치·커밋 (RED / GREEN / REFACTOR)

- **브랜치 이름**: 스토리·에픽 단위로 하나 두고, **RED 단계**임을 드러내려면 접두사 **`red/`** 를 쓴다. 권장 형식은 `red/US-###-<짧은-슬러그>` 또는 에픽 단위가 명확하면 `red/epic-001-<슬러그>`이다. 기존 이름이 이미 `red/…` 이면 그대로 RED 브랜치로 간주해도 된다 (예: `red/dual-track-test-cases`). US 추적을 이름에 넣으려면 `git branch -m red/US-006-dual-track-test-cases` 처럼 로컬에서만 바꿔도 된다.
- **커밋**: 같은 브랜치 안에서 RED→GREEN→REFACTOR를 **커밋으로 분리**한다 (예: `test(...)` → `feat(...)` → `refactor(...)`). GREEN·REFACTOR 단계로 넘어가도 브랜치 이름을 꼭 바꿀 필요는 없고, 머지 후 다음 스토리용 새 브랜치를 만들면 된다.

---

## 검증 기준 (PRD 중심)

| 구분 | 기준 |
|------|------|
| 기능 | FR-01 ~ FR-05 및 각 AC (PRD §5) |
| 비기능 | NFR-01 ~ NFR-04: 도메인/경계 커버리지, 결정론, **호출자 행렬 비변경** |
| 테스트 계획 | PRD §9 — 시나리오 TP-01~TP-07, 시드 A/B/C, 추적 §12 |

---

## 구현 To-Do

PRD **FR·AC·§12 Traceability** 및 Report/4 스토리 순서에 맞춘 체크리스트입니다.

### Epic

- [ ] **Epic-001:** Invariant·계약 기준 4×4 부분 완성 시스템 — FR-01~FR-05 완료, Dual-Track 유지, §7 NFR 충족

### User Story 단위

- [ ] **US-001** 입력 검증 (FR-01): 스키마 위반 시 도메인 미호출 — AC-01~05
- [ ] **US-002** 빈칸 탐색 (FR-02): row-major, 1-index 두 좌표 — AC-06~07
- [ ] **US-003** 누락 숫자 (FR-03): 차집합 2개, `n_small` / `n_large` — AC-08~09
- [ ] **US-004** 마방진 판정 (FR-04): 완전 그리드, 합 34 — AC-10~11
- [ ] **US-005** 두 시도·`int[6]` (FR-05): 시도1→시도2, 실패 `E_DOMAIN` — AC-12~14
- [ ] **US-006** 경계–Control–도메인 연결: 검증 후에만 완성 시도, 성공/`int[6]`·오류 일관

### 작업 항목 (세분화)

**도메인·보드**

- [ ] 도메인 상수 (`MAGIC_CONSTANT`, 크기, 값 범위) — BR-06, INV
- [ ] 보드 로드·스냅샷 — 호출자 `int[][]` **비변경** (NFR-04)
- [ ] 빈칸 2개 좌표 (FR-02)
- [ ] 누락 숫자 2개·정렬 쌍 (FR-03)
- [ ] 완전 그리드 마방진 판정 (FR-04)
- [ ] 두 고정 배치 시도·결과 튜플 (FR-05)

**경계**

- [ ] `E_SIZE` / `E_EMPTY_COUNT` / `E_VALUE_RANGE` / `E_DUPLICATE` — 메시지 PRD §8.1 일치
- [ ] 검증 실패 시 도메인 미호출 (AC-05)
- [ ] `E_DOMAIN` 매핑 및 성공 시 `int[6]` 통과

**통합·품질**

- [ ] Control 오케스트레이션 (규칙 중복 없음)
- [ ] pytest 커버리지: PRD §7 도메인 ≥95%, 경계 ≥85% (게이트가 있으면 CI에 반영)
- [ ] 시드 A 및 시드 B·C 픽스처 (PRD §9.3)

---

## 라이선스

저장소에 `LICENSE`가 추가되면 그에 따릅니다.
