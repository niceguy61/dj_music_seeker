# DJ Music Seeker 🎵

DJ Music Seeker는 AWS Bedrock의 Claude 3.5 Sonnet 모델을 활용하여 DJ 파티를 위한 플레이리스트를 생성하고
YouTube에서 음악을 자동으로 다운로드하는 Python 애플리케이션입니다.

## 주요 기능 ✨

- AWS Bedrock을 활용한 AI 기반 플레이리스트 생성
- YouTube 음원 자동 다운로드
- MP3 포맷 변환 및 저장
- 체계적인 파일 관리 시스템

## 시스템 요구사항 🔧

- Python 3.8 이상
- FFmpeg
- AWS SSO 계정 및 적절한 권한
- AWS Bedrock 접근 권한

## 설치 방법 📦

1. 저장소 클론
```bash
git clone https://github.com/yourusername/dj_music_seeker.git
cd dj_music_seeker
```

2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. FFmpeg 설치
- Windows: `choco install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

## 환경 변수 설정 ⚙️

`.env` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 내용을 추가합니다:
```
AWS_PROFILE=sso
OUTPUT_DIR=output
```

## 사용 방법 🚀

1. AWS SSO 로그인 확인
```bash
aws sso login
```

2. 프로그램 실행
```bash
python main.py
```

## 출력 구조 📁
output/
├── YYYYMMDD/
│ └── {random_id}/
│ ├── song1.mp3
│ ├── song2.mp3
│ └── ...

## 주요 설정 🎛️

- BPM 범위: 100-130
- 재생 시간: 2시간
- 선호 장르: House, Drum and Bass, Dubstep, Hip Hop, Pop, Rock, Synth-pop
- 참조 아티스트: Marcross 82-99

## 라이선스 📄

MIT License

## 주의사항 ⚠️

- YouTube 다운로드 시 저작권 관련 법규를 준수해주세요.
- AWS 사용 비용이 발생할 수 있습니다.
- 개인적인 용도로만 사용해주세요.

## 기여 방법 🤝

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request