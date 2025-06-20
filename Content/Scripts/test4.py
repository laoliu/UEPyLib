import debugpy_unreal as du
#du.install_debugpy()
du.start()
print("Debugpy installed successfully.")

import unreal as ue
import sys
import unreal
#import unreal_engine

#worlds = ue.all_worlds()
#world = worlds[1]

# 获取当前玩家控制器
subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world = subsystem.get_game_world()
print(world)
#sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
#print(sub)
game_mode = unreal.GameplayStatics.get_game_mode(world)
o = game_mode
methods_list = [method for method in dir(o)]
print("Methods using dir():", methods_list)
#sub.spawn_actor_from_class(unreal.StaticMeshActor.static_class(), unreal.Vector(0, 0, 50), unreal.Rotator(0, 0, 0))  # 在世界中生成一个静态网格Actor
player_controller = unreal.GameplayStatics.get_player_character(world, 0)  # 获取第一个玩家角色
print(player_controller)
#player_controller = world.get_first_player_controller()
du.breakpoint()
if player_controller is None:
    # 加载PlayerController类
    player_controller_class = unreal.load_class(None, "/Game/BluePrints/BP_PlayerController.BP_PlayerController_C")
    # 生成PlayerController     
    player_controller = unreal.new_object(player_controller_class, None, unreal.Name("SnakeHead"))
    # 生成一个Character作为Pawn
    #pawn_class = unreal.load_class(None, "/Game/Objects/BP_Snake_Head.BP_Snake_Head_C")     
    #pawn = unreal.new_object(pawn_class, None, unreal.Name("SnakeHead"))
    #pawn.set_actor_scale3d(unreal.FVector(0.8, 0.8, 0.2))  # 扁平化处理
    #rotation = unreal.FRotator(0, 0, 0)
    #pawn.set_actor_rotation(rotation)  # 设置初始旋转
    
    #player_controller.posses(pawn)

# 获取本地玩家
#local_player = player_controller.get_local_player()

# 获取EnhancedInputLocalPlayerSubsystem
#input_subsystem = local_player.get_subsystem(unreal.EnhancedInputLocalPlayerSubsystem)
def list2():
    o=ue
    print(o)    
    #methods_list = [method for method in dir(o)  if callable( getattr(o, method)) and not method.startswith("__")]
    methods_list = [method for method in dir(o)]
    print("Methods using dir():", methods_list)

def list3():
    o=ue.load_asset("/Game/Inputs/IA_Move")
    imc=ue.load_asset("/Game/Inputs/IMC_Default")
    #player_controller = ue.get_editor_subsystem(ue.UnrealEditorSubsystem).get_game_world()
    #player_controller = ue.PlayerState.get_player_controller()  # 获取第一个玩家控制器
    #player_controller = ue.GameplayStatics.get_player_character(world, 0)  # 获取第一个玩家角色
    #print(player_controller)
    o = player_controller
    methods_list = [method for method in dir(o)]
    print("Methods using dir():", methods_list)
    subsystem = ue.EnhancedInputLocalPlayerSubsystem
    subsystem.add_mapping_context(imc, 100) 
    print(o)    
    #methods_list = [method for method in dir(o)  if callable( getattr(o, method)) and not method.startswith("__")]
    methods_list = [method for method in dir(o)]
    print("Methods using dir():", methods_list)

def list_all_modules():
    # 1. 内置模块
    builtin_modules = sys.builtin_module_names
    
    # 2. 已加载模块
    loaded_modules = list(sys.modules.keys())
    
    # 3. 输出结果
    print("=== 内置模块 ===")
    print(builtin_modules)
    
    print("\n=== 已加载模块 ===")
    for mod in loaded_modules:
        print(mod)

def int_to_key(key_code: int) -> None:
    # 定义整数到按键名称的映射表
    key_map = {
        1: "A", 2: "B", 3: "C", 4: "D", 5: "E",
        10: "SpaceBar", 11: "LeftMouseButton", 12: "Gamepad_FaceButton_Bottom"
    }
    key_name = key_map.get(key_code)
    if key_name:
        print(unreal.FKey)
        return unreal.key_by_value(key_name)  # 通过名称构造 Key
    #return unreal.Key()  # 无效键

# 使用示例
#key_obj = int_to_key(1)
#print(key_obj.get_name())  # 输出 "SpaceBar"

#if __name__ == "__main__":
    #list_all_modules()
    #list3()