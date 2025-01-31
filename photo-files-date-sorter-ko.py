import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def get_photo_date(image_path):
    """
    이미지 파일의 EXIF 메타데이터에서 원본 촬영 날짜를 추출합니다.

    Args:
        image_path (str): 이미지 파일의 전체 경로

    Returns:
        str | None: 촬영 날짜(예: 'YYYY:MM:DD HH:MM:SS').
                날짜 정보를 찾을 수 없거나 오류가 발생하면 None을 반환합니다.

    기능:
        - Pillow 라이브러리를 사용하여 이미지 파일을 엽니다.
        - EXIF 메타데이터를 검색합니다.
        - 'DateTimeOriginal' 태그에서 촬영 날짜를 추출합니다.
        - EXIF 데이터가 없거나 오류가 발생할 경우 예외를 처리합니다.

    """
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return value
    except Exception as e:
        print(f"이미지 EXIF 데이터 읽기 오류 {image_path}: {e}")
    return None


def organize_photos_by_date(input_folder_path):
    """
    사진 파일을 촬영 날짜 기준으로 년-월 폴더에 정리합니다.

    Args:
        input_folder_path (str): 사진 파일이 포함된 루트 디렉토리 경로

    워크플로우:
        1. 'sorted-folder'와 'no-date' 하위 디렉토리 생성
        2. 입력 폴더를 재귀적으로 스캔하여 이미지 파일을 검색
        3. EXIF 메타데이터에서 사진 촬영 날짜를 추출
        4. 폴더로 파일 이동:
            - 촬영 날짜가 있는 파일: 년-월 형식의 이름 폴더로 이동
            - 촬영 날짜가 없는 파일: 'no-date' 폴더로 이동

    처리 방식:
        - 숨김 파일 및 시스템 파일 건너뛰기 (예: `.DS_Store`)
        - 파일 이동에 대한 콘솔 출력
        - 파일 이동 중 발생할 수 있는 오류를 처리
    """
    # 정렬된 폴더와 날짜 없는 하위 폴더 생성
    if not os.path.exists(save_sorted_folder):
        os.makedirs(save_sorted_folder)

    no_date_folder = os.path.join(save_sorted_folder, 'no-date')
    os.makedirs(no_date_folder, exist_ok=True)

    # 메인 폴더 스캔, 숨겨진 및 시스템 폴더 무시
    for folder_name in os.listdir(input_folder_path):
        if folder_name.startswith('.') or folder_name == 'sorted-folder':
            continue

        folder_path = os.path.join(input_folder_path, folder_name)

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.startswith('.'):
                    continue

                file_path = os.path.join(folder_path, filename)

                if os.path.isfile(file_path):
                    photo_date = get_photo_date(file_path)

                    if photo_date:
                        try:
                            date_obj = datetime.strptime(photo_date, '%Y:%m:%d %H:%M:%S')
                            year_month = date_obj.strftime('%Y-%m')
                        except ValueError:
                            continue

                        target_folder = os.path.join(save_sorted_folder, year_month)
                        os.makedirs(target_folder, exist_ok=True)

                        try:
                            shutil.move(file_path, os.path.join(target_folder, filename))
                            print(f"{filename}을 {target_folder}로 이동")
                        except Exception as e:
                            print(f"{filename} 이동 중 오류: {e}")
                    else:
                        try:
                            shutil.move(file_path, os.path.join(no_date_folder, filename))
                            print(f"{filename}을 {no_date_folder}로 이동")
                        except Exception as e:
                            print(f"{filename} 이동 중 오류: {e}")


# 구성
main_folder = '/Users/michael/PycharmProjects/utility/temp'
save_sorted_folder = os.path.join(main_folder, 'sorted-folder')
os.makedirs(save_sorted_folder, exist_ok=True)

# 실행
organize_photos_by_date(main_folder)