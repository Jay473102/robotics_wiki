아래처럼 자료를 다시 구성하는 게 좋습니다. 핵심 수정점은 **시뮬레이션에서 온도–마찰 관계를 학습하지 않는다**는 것입니다. 시뮬레이션은 오직 **동역학 역추정 구조**, 즉 “이 $q,\dot q,\tau$ 관계가 어떤 end-effector 관성 $\pi_E$와 effective friction $\phi_f^{eff}$에서 나오는가”를 학습시키는 데만 씁니다. 온도–마찰 baseline은 반드시 **실로봇 정상 데이터**에서 별도로
# 자료 제목

**충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론**

부제:

**Simulation-based Neural Posterior Estimation + Differentiable Dynamics + Real Temperature-Friction Baseline**

---

# 1. 연구 배경

산업용 로봇의 고장진단에서 관절 마찰 파라미터는 매우 중요한 health feature가 될 수 있습니다. 일반적인 로봇 동역학은 다음과 같이 표현됩니다.

$$
\tau

= M(q)\ddot q  
+  
C(q,\dot q)\dot q  
+  
G(q)  
+  
\tau_f(\dot q)  
$$

여기서 $\tau$는 관절 토크, $q,\dot q,\ddot q$는 관절 위치·속도·가속도, (M,C,G)는 각각 관성·코리올리/원심·중력항, $\tau_f$는 마찰항입니다.

전통적인 동역학 식별에서는 위 식을 다음과 같은 선형 regressor 형태로 바꿉니다.

$$
\tau

= Y(q,\dot q,\ddot q)p  
$$

여기서 (p)는 링크 질량, 질량중심, 관성텐서, Coulomb friction, viscous friction, motor inertia 등을 포함한 동역학 파라미터입니다. 업로드한 Raviola et al. 논문도 (Y_{id}, Y_c, Y_v, Y_{I,m}) 네 개 block으로 regressor를 구성하고, Coulomb friction은 $\tanh(\dot q/0.001)$, viscous friction은 $\dot q$, motor inertia는 $\ddot q$에 대응시킵니다.

이 방식의 장점은 해석성이 높다는 점입니다. 예를 들어 식별된 Coulomb friction과 viscous friction coefficient가 증가하면 관절 베어링, 감속기, 윤활 상태 악화와 관련된 health indicator로 쓸 수 있습니다. Raviola et al.도 Coulomb friction과 viscous friction coefficient가 fully identifiable하며, 이 값을 관절 health status 추정에 사용할 수 있다고 설명합니다.

그러나 이 방식은 **충분 가진 persistent excitation trajectory**를 요구합니다. 논문에서는 5차 Finite Fourier Series 기반 궤적을 만들고, regressor condition number를 최소화하는 방향으로 excitation trajectory를 최적화합니다.

문제는 실제 산업 현장에서는 이런 궤적을 수행하기 어렵다는 것입니다. 특히 end-effector가 크거나, 주변 설비와 충돌 위험이 있거나, 작업 motion 자체가 작은 경우에는 큰 가진 궤적을 실행하기 어렵습니다. Raviola et al.도 tool이 장착되면 dynamic parameter를 다시 업데이트해야 하고, tool이 bulky하면 충돌 회피를 위해 기존 persistent trajectory를 그대로 쓰기 어려울 수 있다고 지적합니다.

따라서 본 연구의 문제 정의는 기존과 다릅니다.

$$
\text{기존 목표: Full dynamic parameter identification}  
$$

$$
\text{제안 목표: Small-motion 기반 tool inertia + effective friction + friction fault 추정}  
$$

즉, 로봇 전체 base parameter를 작은 움직임으로 모두 다시 식별하려는 것이 아니라, 다음 세 가지를 분리해서 추정합니다.

$$
\beta_R^0

= \text{사전 식별된 로봇 본체 파라미터}  
$$

$$
\pi_E

= \text{unknown end-effector 관성 파라미터}  
$$

$$
\phi_f^{eff}

= \text{현재 토크를 설명하는 effective friction}  
$$

그리고 최종 고장진단 feature는 다음입니다.

$$
\Delta\phi_f^{fault}

= \phi_f^{eff}

- g^{real}(T)  
$$

여기서 (g^{real}(T))는 실로봇 정상 데이터로 만든 온도–마찰 baseline입니다.

---

# 2. 기존 방법의 한계

## 2.1 충분 가진 trajectory의 현장 적용성 문제

전통적인 regressor 기반 식별은 $Y(q,\dot q,\ddot q)$의 condition number를 낮추기 위해 관절 전 범위를 충분히 움직이는 trajectory를 요구합니다. 논문에서도 FFS 계수 (a_{i,l}, b_{i,l})를 최적화해 모든 base dynamic parameter를 지속적으로 excite하는 trajectory를 설계합니다.

하지만 bulky end-effector가 달린 경우 다음 문제가 생깁니다.

$$
\text{큰 관절 motion}  
\Rightarrow  
\text{큰 TCP sweep}  
\Rightarrow  
\text{충돌 위험 증가}  
$$

또한 작업 자체가 작은 범위에서 이루어지는 경우, 고장진단을 위해 매번 큰 식별 trajectory를 수행하는 것은 생산성·안전성 측면에서 어렵습니다.

---

## 2.2 End-effector 관성 파라미터 unknown 문제

로봇 본체 파라미터는 한 번 offline에서 비교적 안전하게 식별할 수 있습니다. 그러나 실제 작업에서는 end-effector가 바뀔 수 있고, 그 관성 파라미터는 제조사 로봇 모델에 포함되어 있지 않습니다.

end-effector는 마지막 링크의 extension처럼 볼 수 있으므로 자유도는 추가되지 않지만, 마지막 링크 및 상위 관절 토크에는 영향을 줍니다. 따라서 tool 장착 후에는 $\pi_E$를 별도 추정해야 합니다. Raviola et al.도 tool이 장착되면 torque estimate를 맞추기 위해 dynamic parameter update가 필요하다고 설명합니다.

문제는 작은 움직임에서는 $\pi_E$와 $\phi_f$가 residual torque에서 서로 섞일 수 있다는 점입니다.

$$
\Delta\tau

= Y_E(q,\dot q,\ddot q)\Delta\pi_E  
+  
Y_f(\dot q)\Delta\phi_f  
+  
\epsilon  
$$

따라서 tool inertia와 friction fault를 같은 window에서 동시에 자유롭게 추정하면 안 됩니다. 둘은 시간 스케일을 분리해야 합니다.

$$
\pi_E  
:  
\text{tool 장착 시 느리게 추정}  
$$

$$
\phi_f^{eff},\Delta\phi_f^{fault}  
:  
\text{작업 중 빠르게 추정}  
$$

---

## 2.3 온도–마찰 관계는 시뮬레이션으로 만들 수 없음

이 부분이 가장 중요합니다.

마찰계수, 특히 viscous friction은 온도에 크게 영향을 받습니다. Raviola et al.은 UR3와 UR5에서 동일 trajectory를 온도 상승 구간에서 반복 수행했고, viscous friction coefficient가 UR3에서 평균 약 20%, UR5에서 약 17% 감소하는 것을 보였습니다. 또한 Figure 8에서는 joint별 온도 상승에 따라 viscous friction coefficient가 감소하는 실측 trend를 보여줍니다.

하지만 이 관계는 로봇·관절·윤활 상태·감속기 상태·누적 사용시간·방열 구조에 따라 달라집니다. 같은 형태의 joint라도 lubrication condition이나 wear에 따라 curve가 달라질 수 있습니다. 논문에서도 UR3 elbow와 UR5 wrist joints의 friction-temperature trend가 유사하지만 완전히 같지는 않고, 그 차이를 윤활 상태나 wear 가능성과 연결해 해석합니다.

따라서 simulation에서 다음을 하면 안 됩니다.

$$
T \rightarrow \phi_f  
$$

즉,

$$
\phi_f = aT+b  
$$

같은 가짜 온도–마찰 모델을 시뮬레이션에 넣고 NPE가 그 관계를 학습하게 하면 안 됩니다.

대신 simulation은 다음 관계만 학습해야 합니다.

$$
(q,\dot q,\tau)  
\rightarrow  
(\pi_E,\phi_f^{eff})  
$$

온도는 simulation pretraining에는 넣지 않고, real robot baseline에서만 사용합니다.

---

# 3. 제안 방법의 핵심 아이디어

최종 구조는 다음과 같습니다.

$$
\boxed{  
\text{Simulation: } q,\dot q,\tau \rightarrow \pi_E,\phi_f^{eff}  
}  
$$

$$
\boxed{  
\text{Real calibration: } T \rightarrow g^{real}(T)  
}  
$$

$$
\boxed{  
\text{Diagnosis: } \Delta\phi_f^{fault}

= \phi_f^{eff}

- g^{real}(T)  
}  
$$

즉, simulation은 **effective friction을 역추정하는 능력**을 학습시키는 데 사용하고, 온도에 따른 정상 마찰 변화는 **실로봇 정상 데이터**로만 모델링합니다.

---

# 4. 전체 파라미터 분해

제안 모델은 로봇 torque를 다음처럼 분해합니다.

$$
\hat{\tau}_t

= \tau_R(q_t,\dot q_t,\hat{\ddot q}_t;\beta_R^0)  
+  
\tau_E(q_t,\dot q_t,\hat{\ddot q}_t;\pi_E)  
+  
\tau_f(\dot q_t;\phi_f^{eff})  
+  
r_\eta(h_t)  
$$

여기서,

$$
\tau_R  
$$

는 로봇 본체 동역학 torque입니다. 이 항은 사전 식별된 $\beta_R^0$를 사용합니다.

$$
\tau_E  
$$

는 end-effector 관성으로 인해 추가되는 torque입니다. $\pi_E$는 tool 장착 시 추정해야 합니다.

$$
\tau_f  
$$

는 현재 torque를 설명하는 effective friction torque입니다.

$$
r_\eta  
$$

는 cable drag, backlash, torque bias, unmodeled flexibility 같은 정상 residual입니다. 단, 고장신호를 residual network가 흡수하면 안 되므로 nominal data에서만 학습하고 online update는 제한해야 합니다.

end-effector 관성 파라미터는 일반적으로 다음 10개로 둘 수 있습니다.

$$
\pi_E

= [
m,;  
mc_x,;  
mc_y,;  
mc_z,;  
I_{xx},I_{yy},I_{zz},I_{xy},I_{xz},I_{yz}  
]  
$$

하지만 작은 motion 기반 1차 구현에서는 다음 reduced form이 더 현실적입니다.

$$
\pi_E^{red}

= [
m,;  
mc_x,;  
mc_y,;  
mc_z  
]  
$$

질량과 CoM 1차 모멘트는 quasi-static pose에서도 어느 정도 보이지만, 관성텐서는 충분한 angular acceleration이 없으면 식별성이 낮습니다.

마찰 파라미터는 처음에는 joint별로 다음 정도가 적절합니다.

$$
\phi_{f,j}^{eff}

= [
f_{c,j}^{+},  
f_{c,j}^{-},  
f_{v,j}  
]  
$$

즉, 양의 방향 Coulomb friction, 음의 방향 Coulomb friction, viscous friction입니다.

---

# 5. 이론적 배경 1: Regressor 기반 동역학 식별

전통적인 rigid-body dynamics는 동역학 파라미터에 대해 선형입니다.

$$
\tau

= Y(q,\dot q,\ddot q)p  
$$

이 성질 때문에 LS, WLS, CWLS 같은 방식으로 (p)를 식별할 수 있습니다. Raviola et al.은 SVD와 QR decomposition을 사용해 78개 full parameter 중 독립적인 base dynamic parameter만 남겼고, 지면 장착 UR 로봇의 경우 52개 base parameter가 동역학을 설명한다고 분석했습니다.

식별은 보통 다음 LS로 수행됩니다.

$$
p_B

= (Y_B^TY_B)^{-1}Y_B^T\tau  
$$

논문에서도 이 형태의 LS 식별을 사용합니다.

하지만 이 방식은 (Y_B)가 충분히 좋은 condition을 가져야 합니다. 충분 가진 trajectory가 없으면 (Y_B^TY_B)가 ill-conditioned가 되고, 작은 torque noise가 큰 parameter error로 증폭될 수 있습니다.

따라서 기존 방식은 다음 구조입니다.

$$
\text{충분 가진 trajectory}  
\Rightarrow  
Y_B \text{ well-conditioned}  
\Rightarrow  
p_B \text{ 식별}  
\Rightarrow  
\tau \text{ 예측}  
$$

제안 방식은 이 구조를 다음처럼 바꿉니다.

$$
\text{작은 작업 motion}  
\Rightarrow  
\text{ill-posed inverse problem}  
\Rightarrow  
\text{posterior 추정 + 물리 기반 MAP refinement}  
$$

---

# 6. 이론적 배경 2: Simulation-Based Inference / Neural Posterior Estimation

## 6.1 왜 posterior가 필요한가

작은 motion에서는 하나의 torque waveform을 여러 파라미터 조합이 설명할 수 있습니다.

$$
\Delta\tau

= Y_E\Delta\pi_E  
+  
Y_f\Delta\phi_f  
+  
\epsilon  
$$

따라서 단일 point estimate만 내면 위험합니다. 이 문제는 본질적으로 inverse problem입니다.

우리가 알고 싶은 것은 다음입니다.

$$
p(\theta\mid \mathcal{D})  
$$

여기서,

$$
\theta

= [
\pi_E,\phi_f^{eff}  
]  
$$

$$
\mathcal{D}

= \{q_t,\dot q_t,\tau_t\}_{t=1:T}  
$$

입니다.

Bayes rule은 다음과 같습니다.

$$
p(\theta\mid\mathcal{D})

= \frac{  
p(\mathcal{D}\mid\theta)p(\theta)  
}{  
p(\mathcal{D})  
}  
$$

하지만 robot dynamics simulator에서 likelihood $p(\mathcal{D}\mid\theta)$를 정확히 계산하기 어렵고, noise, delay, unmodeled residual도 존재합니다. Simulation-Based Inference는 이런 “forward simulation은 가능하지만 likelihood 계산은 어려운” 문제를 다룹니다. Cranmer et al.은 복잡한 simulator가 high-fidelity sample은 만들 수 있지만, 그 자체가 statistical inference에 바로 적합하지 않아 inverse problem이 어려워진다고 설명합니다. ([[Cranmer_2020_The_frontier_of_simulation-based_inference.pdf|PNAS]])

Neural Posterior Estimation은 simulator로 만든 데이터 쌍

$$
(\theta^{(i)},\mathcal{D}^{(i)})  
$$

을 이용해 다음 conditional density estimator를 학습합니다.

$$
q_\psi(\theta\mid\mathcal{D})  
\approx  
p(\theta\mid\mathcal{D})  
$$

학습 loss는 다음입니다.

$$
\mathcal{L}_{NPE}

= \sum_i  
\log q_\psi(\theta^{(i)}\mid\mathcal{D}^{(i)})  
$$

Greenberg et al.의 APT는 sequential neural posterior estimation 방법으로, flow-based density estimator와 결합할 수 있고 high-dimensional time-series data에도 적용 가능하다고 설명됩니다. ([[Greenberg_2019_Automatic_Posterior_Transformation_for_Likelihood-Free_Inference.pdf|arXiv]])

로봇 분야에서는 Neural Posterior Domain Randomization이 유사한 방향입니다. 이 방법은 simulator parameter posterior를 Bayesian하게 업데이트하여, 고정된 Gaussian/Uniform domain randomization보다 더 유연한 parameter distribution을 다룰 수 있게 합니다. ([[Muratore_2022_Neural_Posterior_Domain_Randomization.pdf|Proceedings of Machine Learning Research]])

---

## 6.2 본 문제에 맞춘 NPE의 역할

본 연구에서 NPE는 온도–마찰 관계를 학습하지 않습니다.

NPE의 목표는 오직 다음입니다.

$$
q_\psi(\pi_E,\phi_f^{eff}\mid q,\dot q,\tau)  
$$

즉, 입력 window의 torque response를 보고 현재 effective physical parameter를 추정합니다.

이때 simulation에서 생성하는 데이터는 다음과 같습니다.

$$
\pi_E^{(i)}\sim p(\pi_E)  
$$

$$
\phi_f^{eff,(i)}\sim p(\phi_f^{eff})  
$$

$$
q,\dot q,\ddot q\sim p(\text{safe small motions})  
$$

$$
\tau

= \tau_R(\beta_R^0)  
+  
\tau_E(\pi_E^{(i)})  
+  
\tau_f(\phi_f^{eff,(i)})  
+  
\epsilon  
$$

여기서 (T)는 없습니다.

온도는 나중에 실로봇 baseline에서만 사용합니다.

$$
\Delta\phi_f^{fault}

= \phi_f^{eff}

- g^{real}(T)  
$$

이렇게 하면 simulation의 역할과 real calibration의 역할이 분리됩니다.

---

# 7. 이론적 배경 3: Differentiable Dynamics + MAP Refinement

NPE는 작은 window에서 빠르게 posterior를 추정하는 데 유리하지만, simulation-to-real mismatch가 있을 수 있습니다. 따라서 최종 추정값은 differentiable dynamics 기반 MAP refinement로 한 번 더 조정하는 것이 좋습니다.

Differentiable dynamics는 rigid-body dynamics 계산 graph를 미분 가능하게 구현한 뒤, $\pi_E$나 $\phi_f^{eff}$에 직접 gradient를 흘려 torque error를 줄이는 방법입니다.

$$
\theta^*

= \arg\min_\theta  
\mathcal{L}(\theta)  
$$

$$
\theta

= [
\pi_E,\phi_f^{eff}  
]  
$$

$$
\mathcal{L}(\theta)

= \sum_t  
\rho  
\left(  
\tau_t^{meas}

- \hat{\tau}_t(q,\dot q,\hat{\ddot q};\theta)  
\right)  
+  
\lambda_\theta  
|\theta-\theta_0|^2  
$$

여기서 $\rho$는 Huber loss 같은 robust loss가 좋습니다.

Lutter et al.의 DiffNEA는 Newton-Euler algorithm을 differentiable simulator로 구성하고, complex friction model과 constraints를 포함한 real-world mechanical system parameter를 gradient-based optimization으로 식별할 수 있음을 보입니다. 또한 physically consistent parameter를 보장하기 위해 virtual parameterization을 사용합니다. ([[Lutter_2021_A_Differentiable_Newton-Euler_Algorithm_for_Real-World_Robotics.pdf|arXiv]])

본 문제에서 differentiable dynamics는 두 가지 역할을 합니다.

첫째, NPE가 낸 posterior mean 또는 sample을 초기값으로 받아 최종 torque residual을 줄입니다.

$$
\theta_{init}

= \mathbb{E}_{q_\psi}[\theta]  
$$

$$
\theta^*

= \arg\min_\theta  
\mathcal{L}(\theta)  
$$

둘째, Hessian 또는 Fisher information으로 현재 motion의 식별성을 평가합니다.

$$
J_\theta

= \frac{\partial \hat{\tau}}{\partial \theta}  
$$

$$
H

= J_\theta^T\Sigma_\tau^{-1}J_\theta  
+  
\Sigma_\theta^{-1}  
$$

$$
\Sigma_\theta  
\approx  
H^{-1}  
$$

만약 $\Sigma_\theta$가 크거나 (H)가 ill-conditioned이면, 그 window에서는 parameter가 잘 보이지 않는다는 뜻입니다. 이 경우 고장 판단을 보류하거나 작은 diagnostic micro-dither를 요청해야 합니다.

---

# 8. 수정된 전체 아키텍처

최종 시스템은 다음 5단계로 구성합니다.

```text
Stage 0. Robot-body offline identification
    βR0 식별
    로봇 본체 동역학 기준 모델 확보

Stage 1. Simulation pretraining
    πE, φeff를 독립 샘플링
    q, qdot, tau → πE, φeff posterior 학습
    온도 T는 입력하지 않음

Stage 2. Tool calibration
    tool 장착 후 작은 static pose + small dither 수행
    πE posterior 추정
    differentiable MAP로 πE refinement

Stage 3. Real temperature-friction baseline
    정상 로봇 warm-up 데이터 수집
    window별 φeff 추정
    g_real(T) fitting

Stage 4. Online diagnosis
    작업 중 q, qdot, tau window에서 φeff 추정
    Δφfault = φeff - g_real(T)
    uncertainty-aware fault score 산출
```

---

# 9. Stage별 상세 구조

## 9.1 Stage 0 — Robot-body offline identification

로봇 본체 파라미터 $\beta_R^0$는 end-effector가 없는 상태 또는 표준 tool 상태에서 기존 방식으로 식별합니다.

$$
\beta_R^0

= \arg\min_{\beta_R}  
\sum_t  
\left|  
\tau_t

Y_R(q_t,\dot q_t,\ddot q_t)\beta_R  
\right|^2  
$$

이 단계는 한 번만 수행합니다. 현장 고장진단 때마다 반복하지 않습니다.

---

## 9.2 Stage 1 — Simulation pretraining

시뮬레이션에서는 온도–마찰 관계를 만들지 않습니다.

잘못된 방식:

$$
T\sim p(T),\quad \phi_f=aT+b  
$$

올바른 방식:

$$
\phi_f^{eff}\sim p(\phi_f^{eff})  
$$

즉, friction coefficient 자체를 독립적인 latent physical parameter로 샘플링합니다.

학습 데이터 생성:

$$
\pi_E^{(i)}  
\sim p(\pi_E)  
$$

$$
\phi_f^{eff,(i)}  
\sim p(\phi_f^{eff})  
$$

$$
\mathcal{D}^{(i)}

= \{q_t,\dot q_t,\tau_t\}_{t=1:T}  
$$

$$
\tau_t

= \tau_R(\beta_R^0)  
+  
\tau_E(\pi_E^{(i)})  
+  
\tau_f(\phi_f^{eff,(i)})  
+  
\epsilon_t  
$$

NPE 학습 목표:

$$
q_\psi(\pi_E,\phi_f^{eff}\mid\mathcal{D})  
$$

loss:

$$
\mathcal{L}_{NPE}

= \log q_\psi  
\left(  
\pi_E^{true},\phi_f^{eff,true}  
\mid  
\mathcal{D}  
\right)  
$$

추가로 torque reconstruction loss를 둡니다.

$$
\mathcal{L}_\tau

= \sum_t  
\left|  
\tau_t

- \hat{\tau}_t  
\right|^2  
$$

전체 loss:

$$
\mathcal{L}

= \mathcal{L}_{NPE}  
+  
\lambda_\tau\mathcal{L}_\tau  
+  
\lambda_{phys}\mathcal{L}_{phys}  
+  
\lambda_{sep}\mathcal{L}_{sep}  
$$

여기서 $\mathcal{L}_{phys}$는 질량 양수, friction coefficient non-negative, inertia tensor positive definite 같은 물리 제약입니다.

---

## 9.3 Stage 2 — Tool calibration

Tool 장착 후에는 $\pi_E$를 먼저 추정합니다. 이때 friction fault는 없다고 가정합니다.

$$
\Delta\phi_f^{fault}=0  
$$

Tool calibration data:

$$
\mathcal{D}_{tool}

= \{q,\dot q,\tau\}_{1:T_c}  
$$

motion은 큰 persistent excitation이 아니라 다음으로 구성합니다.

```text
여러 static pose
작은 joint dither
저속 +방향 / -방향 움직임
충돌 constraint 내 작업 자세 근처 motion
```

NPE:

$$
q_{\psi_E}(\pi_E\mid\mathcal{D}_{tool})  
$$

MAP refinement:

$$
\pi_E^*

= \arg\min_{\pi_E}  
\sum_t  
\left|  
\tau_t

- \hat{\tau}_t(\beta_R^0,\pi_E,\phi_f^{normal})  
\right|^2  
+  
\lambda_E  
|\pi_E-\pi_E^{prior}|^2  
$$

Tool inertia는 이후 online diagnosis에서 고정합니다.

$$
\pi_E=\pi_E^*  
$$

---

## 9.4 Stage 3 — Real temperature-friction baseline

이 단계가 기존 설명에서 수정된 핵심입니다.

온도–마찰 baseline은 simulation이 아니라 정상 실로봇 데이터에서 만듭니다.

정상 warm-up data를 수집합니다.

```text
cold start
normal operating temperature까지 warm-up
joint temperature Tj 기록
q, qdot, motor current 또는 torque 기록
동일하거나 유사한 micro friction motion 반복
```

각 window에서 effective friction을 추정합니다.

$$
\phi_{f,w}^{eff}

= \arg\min_{\phi_f}  
\sum_{t\in w}  
\left|  
\tau_t

- \tau_R(\beta_R^0)

- \tau_E(\pi_E^*)

- \tau_f(\phi_f)  
\right|^2  
$$

그러면 다음 sample들이 생깁니다.

$$
(T_w,\phi_{f,w}^{eff},\Sigma_{f,w})  
$$

이 sample로 joint별 baseline을 fitting합니다.

$$
g_j^{real}(T)

= \text{fit}  
\left(  
T_{j,w},\phi_{f,j,w}^{eff}  
\right)  
$$

1차 모델은 선형으로 충분할 수 있습니다.

$$
g_{v,j}^{real}(T)

= a_jT+b_j  
$$

하지만 실제 적용에서는 monotonic spline 또는 Gaussian Process가 더 안전합니다.

$$
g_j^{real}(T)  
\sim  
\mathcal{N}  
\left(  
\mu_{g,j}(T),  
\Sigma_{g,j}(T)  
\right)  
$$

중요한 점은 (g^{real}(T))를 hard constraint로 쓰지 않는 것입니다. baseline uncertainty를 같이 둬야 합니다.

---

## 9.5 Stage 4 — Online diagnosis

작업 중 sliding window를 가져옵니다.

$$
\mathcal{D}_{diag}

= \{q_t,\dot q_t,\tau_t\}_{t=1:T_d}  
$$

NPE로 현재 effective friction을 추정합니다.

$$
q_{\psi_f}(\phi_f^{eff}\mid\mathcal{D}_{diag},\pi_E^*)  
$$

MAP refinement:

$$
\phi_f^{eff,*}

= \arg\min_{\phi_f^{eff}}  
\sum_t  
\left|  
\tau_t

\hat{\tau}_t(\beta_R^0,\pi_E^*,\phi_f^{eff})  
\right|^2  
+  
\lambda_f  
|\phi_f^{eff}-\phi_{init}|^2  
$$

그 다음 현재 온도에서 정상 friction baseline을 계산합니다.

$$
\phi_f^{normal}

= g^{real}(T)  
$$

최종 fault component:

$$
\boxed{  
\Delta\phi_f^{fault}

= \phi_f^{eff,*}

- g^{real}(T)  
}  
$$

uncertainty-aware fault score:

$$
S_f

= \Delta\phi_f^{fault,T}  
\left(  
\Sigma_{est}  
+  
\Sigma_g(T)  
+  
\Sigma_{sensor}  
\right)^{-1}  
\Delta\phi_f^{fault}  
$$

이 score가 threshold를 넘으면 fault suspected로 판단합니다.

---

# 10. 학습 구조 상세

## 10.1 입력

NPE 입력은 다음입니다.

$$
x_t

= [
q_t,\dot q_t,\tau_t  
]  
$$

여기서 $\ddot q_t$는 직접 넣지 않아도 됩니다. temporal encoder가 $q,\dot q$ window에서 acceleration latent를 추정하게 합니다.

$$
[q,\dot q]_{t-L:t+K}  
\rightarrow  
\hat{\ddot q}_t  
$$

업로드 논문에서도 UR 로봇이 joint acceleration을 직접 제공하지 않아 velocity를 미분하고 filtering해서 acceleration을 얻었다고 설명합니다.

제안 방식에서는 이 미분/필터링을 직접 하거나, temporal encoder 내부 latent로 둡니다.

---

## 10.2 Temporal encoder

$$
h_{1:T}

= E_\psi(x_{1:T})  
$$

가능한 구조:

```text
TCN
GRU / LSTM
Transformer encoder
```

작은 motion에서 local derivative와 velocity sign change가 중요하므로 1차 구현은 TCN이 적절합니다. Transformer는 데이터가 많을 때 확장하는 편이 좋습니다.

---

## 10.3 Posterior head

출력은 point estimate가 아니라 posterior입니다.

$$
q_\psi(\theta\mid\mathcal{D})  
$$

$$
\theta=[\pi_E,\phi_f^{eff}]  
$$

초기 구현은 diagonal Gaussian으로 충분합니다.

$$
q_\psi(\theta\mid\mathcal{D})

= \mathcal{N}  
(\mu_\psi,\Sigma_\psi)  
$$

고급 구현에서는 normalizing flow를 사용할 수 있습니다. 작은 motion에서는 posterior가 길게 늘어나거나 multi-modal할 수 있기 때문입니다.

---

## 10.4 Physics decoder

posterior에서 sample한 $\theta$를 physics decoder에 넣습니다.

$$
\hat{\tau}_t

= \tau_R(q_t,\dot q_t,\hat{\ddot q}_t;\beta_R^0)  
+  
\tau_E(q_t,\dot q_t,\hat{\ddot q}_t;\pi_E)  
+  
\tau_f(\dot q_t;\phi_f^{eff})  
$$

friction model은 1차적으로 다음처럼 둡니다.

$$
\tau_{f,j}

= f_{c,j}^{+}\tanh  
\left(  
\frac{\dot q_j}{\epsilon}  
\right)  
+  
f_{v,j}\dot q_j  
$$

방향별 Coulomb friction을 분리하면:

$$
\tau_{f,j}

= f_{c,j}^{+}\sigma(\dot q_j)

- f_{c,j}^{-}\sigma(-\dot q_j)  
+  
f_{v,j}\dot q_j  
$$

---

# 11. 수도코드

## 11.1 Simulation pretraining

```python
# =======================================================
# Simulation pretraining
# Temperature-friction relation is NOT simulated.
# =======================================================

for epoch in range(num_epochs):

    for batch in range(num_batches):

        # 1. Sample end-effector inertia
        pi_E_true = sample_tool_inertia_prior()
        # e.g. mass, first moment, optional inertia tensor

        # 2. Sample effective friction directly
        # Do NOT sample temperature.
        # Do NOT generate friction from temperature.
        phi_eff_true = sample_effective_friction_prior()

        # 3. Generate collision-safe small motion
        q, qdot, qddot = generate_safe_motion(
            type=random_choice([
                "static_pose_set",
                "small_dither",
                "low_speed_positive_negative",
                "task_like_motion"
            ]),
            collision_constraints=True,
            joint_limits=True,
            velocity_limits=True
        )

        # 4. Forward dynamics / inverse dynamics torque
        tau_clean = inverse_dynamics(
            q=q,
            qdot=qdot,
            qddot=qddot,
            beta_R=beta_R0,
            pi_E=pi_E_true,
            phi_f=phi_eff_true
        )

        # 5. Add realistic noise, delay, torque bias
        tau = add_noise_delay_bias(tau_clean)
        q_noisy, qdot_noisy = add_encoder_noise(q, qdot)

        D = {
            "q": q_noisy,
            "qdot": qdot_noisy,
            "tau": tau
        }

        # 6. Encode sequence
        h = temporal_encoder(D)

        # 7. Posterior estimation
        posterior = posterior_head(h)
        # posterior over theta = [pi_E, phi_eff]

        loss_npe = -posterior.log_prob({
            "pi_E": pi_E_true,
            "phi_eff": phi_eff_true
        })

        # 8. Optional physics reconstruction
        pi_E_sample, phi_eff_sample = posterior.rsample()

        qddot_hat = accel_estimator(q_noisy, qdot_noisy)

        tau_hat = inverse_dynamics(
            q=q_noisy,
            qdot=qdot_noisy,
            qddot=qddot_hat,
            beta_R=beta_R0,
            pi_E=pi_E_sample,
            phi_f=phi_eff_sample
        )

        loss_tau = mse(tau_hat, tau)

        loss_phys = physical_constraint_penalty(
            pi_E_sample,
            phi_eff_sample
        )

        loss = (
            loss_npe
            + lambda_tau * loss_tau
            + lambda_phys * loss_phys
        )

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

---

## 11.2 Tool calibration

```python
# =======================================================
# Tool calibration after end-effector installation
# =======================================================

def calibrate_tool(D_tool):

    # NPE posterior
    h = temporal_encoder(D_tool)
    posterior = posterior_tool_head(h)

    pi_E_init = posterior.mean()["pi_E"]
    Sigma_E_init = posterior.covariance()["pi_E"]

    # Differentiable MAP refinement
    pi_E = make_trainable_physical_tool_params(pi_E_init)

    optimizer = Adam([pi_E.raw_params], lr=1e-2)

    for step in range(num_steps):

        pi_E_valid = pi_E.to_physical_params()

        qddot_hat = accel_estimator(
            D_tool["q"],
            D_tool["qdot"]
        )

        tau_hat = inverse_dynamics(
            q=D_tool["q"],
            qdot=D_tool["qdot"],
            qddot=qddot_hat,
            beta_R=beta_R0,
            pi_E=pi_E_valid,
            phi_f=nominal_friction_initial
        )

        loss_tau = huber_loss(D_tool["tau"] - tau_hat)

        loss_prior = mahalanobis_prior(
            pi_E_valid,
            mean=pi_E_init,
            cov=Sigma_E_init
        )

        loss_phys = physical_constraint_penalty_tool(pi_E_valid)

        loss = (
            loss_tau
            + lambda_prior_E * loss_prior
            + lambda_phys_E * loss_phys
        )

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    pi_E_star = pi_E.to_physical_params()

    Sigma_E_star = estimate_hessian_covariance(
        params=pi_E.raw_params,
        loss_fn=current_tool_loss
    )

    return pi_E_star, Sigma_E_star
```

---

## 11.3 Real temperature-friction baseline

```python
# =======================================================
# Real temperature-friction baseline
# This is real-data-only.
# =======================================================

def build_real_temperature_baseline(normal_warmup_logs, pi_E_star):

    samples = []

    for D_win in normal_warmup_logs:

        # Estimate effective friction for each window
        phi_eff = make_trainable_friction_params(
            init=nominal_friction_initial
        )

        optimizer = Adam([phi_eff.raw_params], lr=1e-2)

        for step in range(num_steps):

            phi_valid = phi_eff.to_physical_params()

            qddot_hat = accel_estimator(
                D_win["q"],
                D_win["qdot"]
            )

            tau_hat = inverse_dynamics(
                q=D_win["q"],
                qdot=D_win["qdot"],
                qddot=qddot_hat,
                beta_R=beta_R0,
                pi_E=pi_E_star,
                phi_f=phi_valid
            )

            loss_tau = huber_loss(D_win["tau"] - tau_hat)
            loss_prior = weak_friction_prior(phi_valid)

            loss = loss_tau + lambda_phi * loss_prior

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        phi_eff_star = phi_eff.to_physical_params()

        Sigma_phi = estimate_hessian_covariance(
            params=phi_eff.raw_params,
            loss_fn=current_friction_loss
        )

        T_mean = mean(D_win["joint_temperature"], axis="time")

        samples.append({
            "T": T_mean,
            "phi_eff": phi_eff_star,
            "cov": Sigma_phi
        })

    # Fit joint-wise baseline
    g_real = fit_jointwise_temperature_baseline(
        samples=samples,
        model_type="linear_or_monotonic_spline",
        output_uncertainty=True
    )

    return g_real
```

---

## 11.4 Online diagnosis

```python
# =======================================================
# Online diagnosis
# =======================================================

def diagnose_window(D_diag, pi_E_star, g_real):

    # 1. Estimate effective friction from q, qdot, torque
    h = temporal_encoder({
        "q": D_diag["q"],
        "qdot": D_diag["qdot"],
        "tau": D_diag["tau"]
    })

    posterior = posterior_friction_head(h, pi_E_star)

    phi_eff_init = posterior.mean()["phi_eff"]
    Sigma_init = posterior.covariance()["phi_eff"]

    # 2. MAP refine effective friction only
    phi_eff = make_trainable_friction_params(phi_eff_init)

    optimizer = Adam([phi_eff.raw_params], lr=5e-3)

    for step in range(num_steps):

        phi_valid = phi_eff.to_physical_params()

        qddot_hat = accel_estimator(
            D_diag["q"],
            D_diag["qdot"]
        )

        tau_hat = inverse_dynamics(
            q=D_diag["q"],
            qdot=D_diag["qdot"],
            qddot=qddot_hat,
            beta_R=beta_R0,
            pi_E=pi_E_star,
            phi_f=phi_valid
        )

        loss_tau = huber_loss(D_diag["tau"] - tau_hat)

        loss_prior = mahalanobis_prior(
            phi_valid,
            mean=phi_eff_init,
            cov=Sigma_init
        )

        loss = loss_tau + lambda_prior_f * loss_prior

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    phi_eff_star = phi_eff.to_physical_params()

    Sigma_est = estimate_hessian_covariance(
        params=phi_eff.raw_params,
        loss_fn=current_friction_loss
    )

    # 3. Real temperature baseline
    T_current = mean(D_diag["joint_temperature"], axis="time")

    phi_normal, Sigma_g = g_real.predict(T_current)

    # 4. Fault component
    delta_phi_fault = phi_eff_star - phi_normal

    # 5. Information check
    info_score = compute_fisher_information_score(
        D_diag,
        params="friction"
    )

    if info_score < min_info_threshold:
        return {
            "status": "uncertain_insufficient_motion",
            "delta_phi_fault": delta_phi_fault,
            "score": None
        }

    # 6. Uncertainty-aware score
    Sigma_total = Sigma_est + Sigma_g + Sigma_sensor

    fault_score = mahalanobis_score(
        delta_phi_fault,
        Sigma_total
    )

    if fault_score > fault_threshold:
        status = "fault_suspected"
    else:
        status = "normal"

    return {
        "status": status,
        "delta_phi_fault": delta_phi_fault,
        "score": fault_score,
        "uncertainty": Sigma_total
    }
```

---

# 12. 본 방법론의 핵심 차별점

기존 FIGAROH/LS류 접근은 다음 구조입니다.

$$
\text{큰 persistent excitation}  
\Rightarrow  
Y_Bp_B=\tau  
\Rightarrow  
p_B \text{ 식별}  
$$

제안 구조는 다음입니다.

$$
\text{작은 작업 motion}  
\Rightarrow  
q_\psi(\pi_E,\phi_f^{eff}\mid q,\dot q,\tau)  
\Rightarrow  
\text{MAP refinement}  
\Rightarrow  
\Delta\phi_f^{fault}

= \phi_f^{eff}-g^{real}(T)  
$$

핵심 차이는 세 가지입니다.

첫째, full base parameter를 매번 식별하지 않습니다. 로봇 본체는 $\beta_R^0$로 고정하고, tool inertia와 friction만 분리 추정합니다.

둘째, simulation은 온도–마찰 관계를 만들지 않습니다. simulation은 parameter-to-torque inverse mapping만 학습시키고, 온도 baseline은 실로봇 정상 데이터로만 구축합니다.

셋째, 단일 parameter estimate가 아니라 posterior와 uncertainty를 사용합니다. 작은 motion에서 정보가 부족하면 고장이라고 단정하지 않고 “진단 불확실”로 처리할 수 있습니다.

---

# 13. 자료에서 강조할 문장

제안서나 발표자료에는 다음 문장을 핵심으로 쓰면 좋습니다.

> 기존 동역학 파라미터 식별은 충분 가진 trajectory를 요구하므로, 대형 end-effector가 장착된 산업용 로봇이나 협소한 작업공간에서는 충돌 위험으로 적용이 어렵다. 본 연구는 로봇 본체 동역학 파라미터를 사전 식별한 뒤, 작은 작업 motion으로 end-effector 관성 파라미터와 현재 effective friction을 posterior 형태로 추정하고, differentiable dynamics 기반 MAP refinement로 물리적 일관성을 보정한다. 단, 온도–마찰 관계는 시뮬레이션으로 모사하지 않고, 정상 실로봇 warm-up 데이터로 joint별 (g^{real}(T)) baseline을 구축한다. 최종 고장진단 feature는 ( \phi_f^{eff} - g^{real}(T) )로 정의하여 온도 변화와 실제 마찰 열화를 분리한다.

---

# 14. 최종 구조 요약

$$
\boxed{  
\beta_R^0

= \text{robot-only offline identification}  
}  
$$

$$
\boxed{  
q_\psi(\pi_E,\phi_f^{eff}\mid q,\dot q,\tau)

= \text{simulation-pretrained NPE}  
}  
$$

$$
\boxed{  
\pi_E^*

= \text{tool calibration + differentiable MAP}  
}  
$$

$$
\boxed{  
g^{real}(T)

= \text{normal real robot temperature-friction baseline}  
}  
$$

$$
\boxed{  
\Delta\phi_f^{fault}

= \phi_f^{eff,*}

- g^{real}(T)  
}  
$$

$$
\boxed{  
S_f

= \Delta\phi_f^{T}  
(\Sigma_{est}+\Sigma_g+\Sigma_{sensor})^{-1}  
\Delta\phi_f  
}  
$$

이 구조가 지금 문제에 가장 맞습니다. 핵심은 **“simulation으로 temperature-friction을 배우는 것”이 아니라, “simulation으로 friction inverse estimator를 만들고, temperature correction은 real baseline으로 따로 처리하는 것”**입니다.
