from gymnasium.envs.registration import register

register(
    id='FaaSTrainGym-v1',
    entry_point='faas_environments.k8s_faas_env:OpenFaasEnv',
    max_episode_steps=20,
    reward_threshold=1000000.0,
    kwargs={'render_mode': 'tensorflow'}
)
