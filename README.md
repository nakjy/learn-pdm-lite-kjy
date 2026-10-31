# Day5 예지보전 · 노이즈 vs 추세 (10분) — learn-pdm-lite-kjy

설비 센서 데이터(가상 50건)에서 평상 범위(평균 ± 2σ)로 이상 후보를 찾고, 한 번의 튐(노이즈)과 추세적 상승을 구분하는 10분 수업 실습. 수업은 Claude Code 스킬 `/learn-pdm-lite-kjy`가 진행한다 (Skills as Curriculum). 이 강의는 course-forge로 직접 만들었다.

- **결과 대시보드**: https://nakjy.github.io/learn-pdm-lite-kjy/
- 처음이면 [GUIDE.md](GUIDE.md)부터. 기본 환경은 Claude 데스크톱 앱(Code 탭). VS Code는 GUIDE 부록 B

![결과 그래프](.claude/skills/learn-pdm-lite-kjy/assets/answers/preview.png)

## 설치 — 한 줄

Claude Code 입력칸에 붙여 넣는다.

```
npx skills add nakjy/learn-pdm-lite-kjy --agent claude-code --global --yes 를 실행해 줘
```

새 세션에서 `/learn-pdm-lite-kjy`를 입력하면 수업이 시작된다. zip을 받았다면 GUIDE.md 2단계대로 설치한다.

## 블록

| Block | 주제 | 끝나면 생기는 것 |
|---|---|---|
| 0 | 준비 (~2분) | `~/pdm-lite` 작업 폴더 · 센서 데이터 · env_check.txt |
| 1 | 노이즈 vs 추세 (~5분) | anomaly.csv · 진동 그래프 한 장(index.html) · 퀴즈 1문항 |
| 2 | 공개 (~3분) | GitHub Pages 공개 주소 |

## 수업 방식

| 구분 | 내용 |
|---|---|
| 목표 — AI Native | AI에게 맡기는 것이 기본인 방식으로 일한다 |
| 방법 — Skills as Curriculum | 스킬이 블록마다 설명 → 실습 → STOP → 확인·퀴즈를 진행한다 |
| 형식 — 자율학습 | 강사 없이 자기 속도로, 퀴즈로 스스로 점검한다 |

## 원본 강의와 데이터 출처

| 자료 | 출처 | 구분 |
|---|---|---|
| 본 강의 덱 | keerhee/kma-auto-genai-3-1 · Day5_예지보전/Day5_3_Main_자동차예지보전AI활용.pdf (③ 전처리 · ④ 분석1 · 실습과제 2) | 강의 자료 |
| 센서 데이터 | keerhee/kma-auto-genai-3-1 · data/Day5/Day5_설비센서_50건_가상.csv | 가상 |

## 개정 이력

| 날짜 | 바뀐 점 |
|---|---|
| 2026-10-31 | 첫 판 |

## 만든 방법

- `/course-forge`로 만들었다. 제작 기록(원본 요약·커리큘럼·검수 결과)은 `forge/`에 있다.
- 출처: 원본 강의 저장소 https://github.com/keerhee/kma-auto-genai-3-1
