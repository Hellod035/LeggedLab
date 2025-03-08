from legged_lab.envs.base.base_env_config import (  # noqa:F401
    BaseEnvCfg, BaseAgentCfg, BaseSceneCfg, RobotCfg, DomainRandCfg,
    RewardCfg, HeightScannerCfg, AddRigidBodyMassCfg, PhysxCfg, SimCfg
)
from legged_lab.assets.anybotics import ANYMAL_D_CFG
from legged_lab.terrains import GRAVEL_TERRAINS_CFG, ROUGH_TERRAINS_CFG
from isaaclab.managers import RewardTermCfg as RewTerm
import legged_lab.mdp as mdp
from isaaclab.managers.scene_entity_cfg import SceneEntityCfg
from isaaclab.utils import configclass


@configclass
class AnymalDSceneCfg(BaseSceneCfg):
    height_scanner: HeightScannerCfg = HeightScannerCfg(
        enable_height_scan=False,
        prim_body_name="base"
    )
    robot: str = ANYMAL_D_CFG
    terrain_type: str = "generator"
    terrain_generator: str = GRAVEL_TERRAINS_CFG


@configclass
class AnymalDRobotCfg(RobotCfg):
    terminate_contacts_body_names: list = [".*base.*"]
    feet_names: list = [".*FOOT.*"]


@configclass
class AnymalDDomainRandCfg(DomainRandCfg):
    add_rigid_body_mass: AddRigidBodyMassCfg = AddRigidBodyMassCfg(
        enable=True,
        params={
            "body_names": [".*base.*"],
            "mass_distribution_params": (-3.0, 3.0),
            "operation": "add"
        }
    )


@configclass
class AnymalDRewardCfg(RewardCfg):
    track_lin_vel_xy_exp: RewTerm = RewTerm(func=mdp.track_lin_vel_xy_yaw_frame_exp, weight=1.0, params={"std": 0.5})
    track_ang_vel_z_exp: RewTerm = RewTerm(func=mdp.track_ang_vel_z_world_exp, weight=1.0, params={"std": 0.5})
    lin_vel_z_l2: RewTerm = RewTerm(func=mdp.lin_vel_z_l2, weight=-1.0)
    ang_vel_xy_l2: RewTerm = RewTerm(func=mdp.ang_vel_xy_l2, weight=-0.05)
    energy: RewTerm = RewTerm(func=mdp.energy, weight=-1e-3)
    dof_acc_l2: RewTerm = RewTerm(func=mdp.joint_acc_l2, weight=-1.25e-7)
    action_rate_l2: RewTerm = RewTerm(func=mdp.action_rate_l2, weight=-0.01)
    undesired_contacts: RewTerm = RewTerm(func=mdp.undesired_contacts, weight=-1.0, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names="(?!.*FOOT.*).*"), "threshold": 1.0})
    fly: RewTerm = RewTerm(func=mdp.fly, weight=-1.0, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*FOOT.*"), "threshold": 1.0})
    flat_orientation_l2: RewTerm = RewTerm(func=mdp.flat_orientation_l2, weight=-1.0)
    termination_penalty: RewTerm = RewTerm(func=mdp.is_terminated, weight=-200.0)
    feet_air_time: RewTerm = RewTerm(func=mdp.feet_air_time_positive_biped, weight=0.5, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*FOOT.*"), "threshold": 0.4})
    feet_slide: RewTerm = RewTerm(func=mdp.feet_slide, weight=-0.25, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*FOOT.*"), "asset_cfg": SceneEntityCfg("robot", body_names=".*FOOT.*")})
    feet_force: RewTerm = RewTerm(func=mdp.body_force, weight=-3e-3, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*FOOT.*"), "threshold": 400, "max_reward": 400})
    feet_stumble = RewTerm(func=mdp.feet_stumble, weight=-2.0, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*FOOT.*")}, )
    dof_pos_limits: RewTerm = RewTerm(func=mdp.joint_pos_limits, weight=-2.0)


@configclass
class AnymalDFlatEnvCfg(BaseEnvCfg):
    scene: AnymalDSceneCfg = AnymalDSceneCfg()
    robot: AnymalDRobotCfg = AnymalDRobotCfg()
    domain_rand: AnymalDDomainRandCfg = AnymalDDomainRandCfg()
    reward: AnymalDRewardCfg = AnymalDRewardCfg()


@configclass
class AnymalDFlatAgentCfg(BaseAgentCfg):
    experiment_name: str = "anymal_d_flat"
    wandb_project: str = "anymal_d_flat"


@configclass
class AnymalDRoughEnvCfg(BaseEnvCfg):
    scene: AnymalDSceneCfg = AnymalDSceneCfg(
        height_scanner=HeightScannerCfg(
            enable_height_scan=True,
            prim_body_name="base"
        ),
        terrain_generator=ROUGH_TERRAINS_CFG
    )
    robot: AnymalDRobotCfg = AnymalDRobotCfg()
    domain_rand: AnymalDDomainRandCfg = AnymalDDomainRandCfg()
    reward: AnymalDRewardCfg = AnymalDRewardCfg()


@configclass
class AnymalDRoughAgentCfg(BaseAgentCfg):
    experiment_name: str = "anymal_c_rough"
    wandb_project: str = "anymal_c_rough"
