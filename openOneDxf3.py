import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# DXF 파일 로드
doc = ezdxf.readfile('C:/Users/user/Desktop/RO/dxf/test4.dxf')

# Modelspace 가져오기
msp = doc.modelspace()

# 모든 라인,원 도형 찾기
lines = msp.query('LINE')
circles = msp.query('CIRCLE')
arcs = msp.query('ARC')
# DXF 파일에서 모든 SPLINE 도형 검색
# splines = dxf_file.modelspace().query("SPLINE")
splines = msp.query("SPLINE")
# DXF 파일에서 모든 LWPOLYLINE 도형 검색
lwpolylines = msp.query("LWPOLYLINE")

# PDF 파일 생성
pdf = canvas.Canvas('lines4.pdf')

# 도면의 가로, 세로 길이 구하기
max_x = max([line.dxf.start[0] for line in lines] + [line.dxf.end[0] for line in lines])
max_y = max([line.dxf.start[1] for line in lines] + [line.dxf.end[1] for line in lines])

# 도면 비율 계산하기
ratio = max_x / max_y

# PDF 페이지 크기 설정하기
page_width = 30000
page_height = int(page_width / ratio)
pdf.setPageSize((page_width, page_height))

# 모든 텍스트 객체들을 PDF에 추가
for entity in msp:
    if entity.dxftype() == 'TEXT':
        # 텍스트 내용과 위치 추출
        text = entity.dxf.text
        text_x, text_y = entity.dxf.insert[0], entity.dxf.insert[1]
        # PDF 파일 중앙으로 옮기기
        pdf_x = text_x + ((page_width - max_x) / 2)
        pdf_y = text_y + ((page_height - max_y) / 2)
        pdf.setFontSize(300)
        # 텍스트 추가
        pdf.drawString(pdf_x, pdf_y, text)


# 모든 라인 객체들의 시작점과 끝점을 이용하여 PDF에 추가
for entity in msp:
    if entity.dxftype() == 'LINE':
        start_x, start_y, end_x, end_y = entity.dxf.start[0], entity.dxf.start[1], entity.dxf.end[0], entity.dxf.end[1]
        # PDF 파일 중앙으로 옮기기
        pdf_x = start_x + ((page_width - max_x) / 2)
        pdf_y = start_y + ((page_height - max_y) / 2)
        pdf_x2 = end_x + ((page_width - max_x) / 2)
        pdf_y2 = end_y + ((page_height - max_y) / 2)
        pdf.line(pdf_x, pdf_y, pdf_x2, pdf_y2)

# 모든 원 객체들의 중심점과 반지름을 이용하여 PDF에 추가
for entity in circles:
    center_x, center_y = entity.dxf.center[0], entity.dxf.center[1]
    radius = entity.dxf.radius
    # PDF 파일 중앙으로 옮기기
    pdf_x = center_x + ((page_width - max_x) / 2)
    pdf_y = center_y + ((page_height - max_y) / 2)
    pdf.circle(pdf_x, pdf_y, radius)

# 모든 ARC 객체들의 중심점, 반지름, 시작각도, 끝각도를 이용하여 PDF에 추가
for entity in arcs:
    center_x, center_y = entity.dxf.center[0], entity.dxf.center[1]
    radius = entity.dxf.radius
    start_angle = entity.dxf.start_angle
    end_angle = entity.dxf.end_angle
    # PDF 파일 중앙으로 옮기기
    pdf_x = center_x + ((page_width - max_x) / 2)
    pdf_y = center_y + ((page_height - max_y) / 2)
    # ARC 그리기
    pdf.arc(pdf_x - radius, pdf_y - radius, pdf_x + radius, pdf_y + radius, start_angle, end_angle)




# 모든 lwpolylines 객체들의 점들을 이용하여 PDF에 추가
for entity in lwpolylines:
    vertices = entity.get_points('xy')
    # vertices 리스트에 저장된 점들을 순서대로 연결하여 lwpolyline 도형 완성
    for i in range(len(vertices) - 1):
        start_x, start_y, end_x, end_y = vertices[i][0], vertices[i][1], vertices[i+1][0], vertices[i+1][1]
        # PDF 파일 중앙으로 옮기기
        pdf_x = start_x + ((page_width - max_x) / 2)
        pdf_y = start_y + ((page_height - max_y) / 2)
        pdf_x2 = end_x + ((page_width - max_x) / 2)
        pdf_y2 = end_y + ((page_height - max_y) / 2)
        pdf.line(pdf_x, pdf_y, pdf_x2, pdf_y2)
    # 마지막 점과 첫 번째 점을 연결하여 폐곡선 완성
    start_x, start_y, end_x, end_y = vertices[-1][0], vertices[-1][1], vertices[0][0], vertices[0][1]
    pdf_x = start_x + ((page_width - max_x) / 2)
    pdf_y = start_y + ((page_height - max_y) / 2)
    pdf_x2 = end_x + ((page_width - max_x) / 2)
    pdf_y2 = end_y + ((page_height - max_y) / 2)
    pdf.line(pdf_x, pdf_y, pdf_x2, pdf_y2)



# 모든 ELLIPSE 객체들의 중심점, 장축 길이, 단축 길이, 회전 각도를 이용하여 PDF에 추가
for entity in msp:
    if entity.dxftype() == 'ELLIPSE':
        center_x, center_y = entity.dxf.center[0], entity.dxf.center[1]
        major_axis = entity.dxf.major_axis
        minor_axis = entity.dxf.minor_axis
        rotation = entity.dxf.rotation
        # PDF 파일 중앙으로 옮기기
        pdf_x = center_x + ((page_width - max_x) / 2)
        pdf_y = center_y + ((page_height - max_y) / 2)
        # ELLIPSE 그리기
        pdf.saveState()
        pdf.translate(pdf_x, pdf_y)
        pdf.rotate(rotation)
        pdf.scale(major_axis, minor_axis)
        pdf.arc(0, 0, 1, 0, 360)
        pdf.restoreState()


# 각 SPLINE 도형에 대해 PDF 파일 중앙에 표시
for spline in splines:
    # SPLINE 도형의 제어점 가져오기
    control_points = spline.control_points
    # 중간 점 찾기
    mid_x = (max([p[0] for p in control_points]) + min([p[0] for p in control_points])) / 2
    mid_y = (max([p[1] for p in control_points]) + min([p[1] for p in control_points])) / 2
    # PDF 파일 중앙에 SPLINE 도형 그리기
    pdf.drawInlineImage("spline.png", mid_x*mm-50, mid_y*mm-50, 100, 100)

# MTEXT 도형 찾기
for entity in msp:
    if entity.dxftype == 'MTEXT':
        # MTEXT 도형의 위치 계산
        x, y = entity.insert
        w, h = entity.width, entity.height
        mtext_center_x, mtext_center_y = x + w / 2, y + h / 2

        # MTEXT 도형의 중앙 위치를 PDF 캔버스 중앙에 맞추기 위한 좌표 계산
        dx, dy = center_x - mtext_center_x, center_y - mtext_center_y

        # MTEXT 도형 그리기
        pdf.drawString(x + dx, y + dy, entity.plain_text())

# PDF 파일 저장
pdf.save()




