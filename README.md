# 2023_1_Capston_Project

2023년 1학기 **캡스턴 프로젝트** - **Inverse Kinematics**와 **로봇팔**을 통한 **하노이탑 놀이**

## 프로젝트 소개
**카메라**와 **학습된 모델**을 통해를 통해 현재 **하노이탑의 상태**를 인식하고, 그에 따라 순서에 맞는 다음 동작(원반을 옮기는 동작)을 수행하는 **3차원 5관절 로봇팔** 제작

<img src="https://github.com/Taebee00/2023_1_Capstone_Project/assets/104549849/10b20ef3-4972-4742-b161-7642806729a8" width="50%" height="50%"/>


> 시연 동영상 링크: https://www.youtube.com/watch?v=ozFXrJzOaL8

## 프로젝트 팀원
|이름|역할|GitHub|
|---|---|---|
|김선우|Inverse Kinematics 계산 & 하노이탑 알고리즘 구현 |https://github.com/sw801733|
|나영조|Inverse Kinematics 수식 계산 & Object Detection 학습 환경 구축 및 학습 진행|https://github.com/Taebee00|
|서종현|HW(로봇팔 프레임) 3D 모델링 및 프린팅 & 하노이탑 알고리즘 구현 & 코드 리팩토링|https://github.com/surpise|
|정우영|HW(로봇팔 프레임) 3D 모델링 및 프린팅 & Object Detection 학습 환경 구축 및 학습 진행|https://github.com/wooyoungman|

## 프로젝트 기간
2023.03.02 ~ 2023.06.02

## 프로젝트 내용
### HW 구성
|![image](https://github.com/Taebee00/2023_1_Capstone_Project/assets/104549849/0e3bf328-24cd-47c8-afa8-b4cc14b1d5e4)|![image](https://github.com/Taebee00/2023_1_Capstone_Project/assets/104549849/add89f6b-28b4-4804-b896-cd27cafe3a84)|
|---|---|

|구성|역할|
|---|---|
|카메라|하노이탑의 현재 상태의 이미지로로 받아오는 역할 수행|
|1번 관절|원통 안에서 $z$축 중심으로 ${R_z}$회전하는 관절(방향 제어)|
|2번 관절|1번 관절에 붙어서 $x$축 또는 $y$축 중심으로 ${R_x}$ 또는 ${R_y}$ 회전하는 관절(높이, 길이 제어)|
|3번 관절|2번 관절에 붙어서 $x$축 또는 $y$축 중심으로 ${R_x}$ 또는 ${R_y}$ 회전하는 관절(높이, 길이 제어)|
|4번 관절|3번 관절에 붙어 5번 관절, 즉 그리퍼의 수평을 맞추기 위해 $x$축 또는 $y$축 중심으로 ${R_x}$ 또는 ${R_y}$ 회전하는 관절(수평 제어)
|5번 관절|4번 관절에 붙어 하노이탑 원반을 잡거나 놓을 수 있도록 회전하는 관절(그리퍼 제어)|

### Inverse Kinematics
로봇팔의 경우, 원하는 위치로 이동시키기 위해서는 각 관절의 각도를 알고 좌표를 계산하는 것(정기구학)이 아닌, 좌표가 주어졌을 때, 그에 맞는 각 관절의 각도를 계산하는**Inverse Kinematics(역기구학)**이 필요함 
> **Inverse Kinematics(역기구학)이란?**
역기구학이란 정기구학의 반대로, 관절을 가진 로봇을 원하는 좌표에 위치시키기 위해 관절의 각도를 조절하기 위한 학문을 말한다. 순기구학의 반대로, 순기구학은 관절의 각도에 따른 위치를 계산하는 것이고, 역기구학은 위치에 따른 관절의 각도를 계산하는 것이다.

- 1,2,3번 이렇게 3개의 관절을 통해 3차원 3관절 Inverse Kinematics를 계산하고, 계산한 값을 통해 4번 관절로 그리퍼의 수평을 맞춘다. 
- 2차원 2관절 Inverse Kinematics를 먼저 계산한 뒤, 그 결과를 활용하여 3차원 3관절 Inverse Kinematics를 계산하였다.

|2차원 2관절 Inverse Kinematics|3차원 3관절 Inverse Kinematics|
|---|---|
|![image](https://github.com/Taebee00/2023_1_Capstone_Project/assets/104549849/bf079a34-b618-48d7-af05-6d289893605b)|![image](https://github.com/Taebee00/2023_1_Capstone_Project/assets/104549849/7718afc1-2bd6-47d6-b79d-c4da703abd61)|
|**1. $\theta_2$ 구하기**<br>  - $cos$ 법칙 사용: $c^2=a^2+b^2-2ab{cos}C$<br>  - $(x^2+y^2)={l_1}^2+{l_2}^2-2l_1l_2cos(180-\theta_2)$<br>  - $cos(180-\theta_2)=-cos(\theta_2)$<br>  - $cos(\theta_2)=\frac{x^2+y^2-{l_1}^2-{l_2}^2}{2l_1l_2}$<br>  - $\theta_2=arccos(\frac{x^2+y^2-{l_1}^2-{l_2}^2}{2l_1l_2})$<br><br>**2. $\theta_1$ 구하기**<br>  - $sin$ 법칙 사용: $\frac{sinB}{b}=\frac{sin C}{c}$<br> - $\frac{sin\bar{\theta_1}}{l_2}=\frac{sin(180-\theta_2)}{\sqrt{x^2+y^2}}=\frac{sin(\theta_2)}{\sqrt{x^2+y^2}}$<br>  - $\bar{\theta_1}=arcsin(\frac{l_2sin(\theta_2)}{\sqrt{x^2+y^2}})$<br>  - $\theta_1=\bar{\theta_1}+\alpha$<br>  - $\alpha=arctan(\frac{y}{x})$<br>  - $\theta_1=arcsin(\frac{l_2sin(\theta_2)}{\sqrt{x^2+y^2}})+arctan(\frac{y}{x})$|**1. $\theta_0$ 구하기**<br>  - $tan(\theta_0)=\frac{y}{x}$<br>  - $\theta_0=arctan(\frac{y}{x})$<br><br>**2. $\theta_1,\theta_2$ 구하기**<br>2차원 좌표 $(\sqrt{x^2+y^2},z)$ 를 기준으로 2차원 2관절 Inverse Kinematics 진행<br>  - $\theta_2=arccos(\frac{x^2+y^2+z^2-l_1^2-l_2^2}{2l_1l_2})$<br>  - $\theta_1=arcsin(\frac{l_2*sin\theta_2}{x^2+y^2+z^2})+arctan(\frac{z}{\sqrt{x^2+y^2}})$|

#### 3차원 3관절 Inverse Kinematic

- $\theta_0$ 구하기
    - $tan(\theta_0)=\frac{y}{x}$
    - $\theta_0=arctan(\frac{y}{x})$
- $\theta_1,\theta_2$ 구하기
    - 2차원 좌표 $(\sqrt{x^2+y^2},z)$ 를 기준으로 2차원 2관절 Inverse Kinematics 진행
        - $\theta_2=arccos(\frac{x^2+y^2+z^2-l_1^2-l_2^2}{2l_1l_2})$
        - $\theta_1=arcsin(\frac{l_2*sin\theta_2}{x^2+y^2+z^2})+arctan(\frac{z}{\sqrt{x^2+y^2}})$
