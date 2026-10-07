# AGENTS.md

이 Repository를 수정하는 AI coding agent는 작업 전에 아래 문서를 순서대로 읽습니다.

1. `PROJECT_GUIDE.md`
2. `HTML_DESIGN_RULES.md`
3. 수정 대상 HTML/CSS와 바로 앞뒤 슬라이드
4. 관련 asset 및 `assets/SOURCES.md`

## Core Rules

- 대상은 Vision AI를 처음 접하는 비전공자입니다.
- 한 슬라이드에는 하나의 핵심 메시지만 둡니다.
- 긴 텍스트보다 그림, Diagram, 수치 예시를 우선합니다.
- Input → Process → Output 흐름이 시각적으로 보여야 합니다.
- 전문 용어는 직관적 설명 뒤에 소개합니다.
- 정확한 구조/관계는 HTML/SVG Diagram을 우선합니다.
- 실제 장면은 Repository 내부 이미지 asset을 우선합니다.
- 생성 이미지를 실제 실험 결과처럼 표현하지 않습니다.
- 공통 CSS는 `docs/slide.css`를 우선 재사용합니다.
- 외부 CDN을 새로 추가하지 않습니다.
- 내용이 많을 때 font를 줄이기보다 슬라이드를 나눕니다.
- 발표 화면에서 overflow, clipping, overlap을 허용하지 않습니다.
- 변경 후 사용하지 않는 CSS/JS를 정리합니다.

## Instruction Priority

충돌 시 다음 순서를 따릅니다.

1. 현재 사용자의 명시적 요청
2. `PROJECT_GUIDE.md`
3. `HTML_DESIGN_RULES.md`
4. 기존의 일관된 슬라이드 스타일
5. 과거 TODO 문서

과거 TODO가 현재 가이드와 충돌하면 TODO를 그대로 구현하지 않습니다.

## Before Editing

- 최신 branch 상태를 확인합니다.
- 대상 슬라이드만 보지 말고 앞뒤 슬라이드를 확인합니다.
- 기존 asset과 class를 재사용할 수 있는지 먼저 확인합니다.
- 새로운 Figure가 필요한 경우 목적을 먼저 정의합니다.
- 수식, Tensor shape, 숫자 예시는 실제 의미를 검증합니다.

## After Editing

반드시 다음을 확인합니다.

- HTML 구조
- CSS syntax
- asset 경로
- slide-number 순서
- viewport overflow
- text/figure overlap
- 최소 글자 가독성
- 공통 CSS 변경의 다른 페이지 영향
- GitHub Pages 배포 결과

작업 결과를 보고할 때는 변경 파일과 핵심 변경 이유를 짧게 요약합니다.
