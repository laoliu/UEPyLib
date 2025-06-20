import unreal
#ue.log(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world())
#o = unreal.Package
#o = unreal.PlayerState.get_player_controller
#o = unreal.EnhancedPlayerInput
#o=unreal.Key.set_editor_property
o = unreal.engine
#o.set_editor_properties(, "key",87)
#o=unreal.FKey("A")
print(o)
#print(unreal.Key.cast(87))
#methods_list = [method for method in dir(o)  if callable( getattr(o, method)) and not method.startswith("__")]
methods_list = [method for method in dir(o)]
print("Methods using dir():", methods_list)

o = unreal.InputMappingContext()
print(o)
methods_list = [method for method in dir(o)]
print("Methods using dir():", methods_list)


move_forward_action = unreal.InputAction()
move_forward_action.set_editor_property("ValueType", unreal.InputActionValueType.AXIS1D)
o.map_key(move_forward_action, unreal.Key(87))
#o = unreal.load_object(None,"/Game/Objects/BP_Snake_Head")
#print(o)
#print(o.generated_class())
#methods_list = [method for method in dir(o)  if callable( getattr(o, method)) and not method.startswith("__")]
#print("Methods using dir():", methods_list)
#classes = unreal.all_classes(world)
#for cls in classes:
#    print(cls)
worlds = unreal.all_worlds()
world = worlds[1]
cls = unreal.load_class(None,"/Game/Objects/BP_Snake_Head.BP_Snake_Head_C")
print(cls)
obj = unreal.new_object(cls, None, unreal.Name("SnakeBody"))
print(obj)

#import unreal

def setup_wasd_mappings():
    # 创建输入动作(Input Actions)
    move_forward_action = unreal.InputAction()
    move_forward_action.set_editor_property("ValueType", unreal.InputActionValueType.AXIS1D)
    
    move_right_action = unreal.InputAction()
    move_right_action.set_editor_property("ValueType", unreal.InputActionValueType.AXIS1D)

    # 创建输入映射上下文(Input Mapping Context)
    mapping_context = unreal.InputMappingContext()
    
    # 绑定WASD到对应动作
    mapping_context.map_key(move_forward_action, unreal.Key.W)  # 前进
    mapping_context.map_key(move_forward_action, unreal.Key.S)  # 后退(自动取负值)
    mapping_context.map_key(move_right_action, unreal.Key.D)    # 右移 
    mapping_context.map_key(move_right_action, unreal.Key.A)    # 左移(自动取负值)

    # 获取增强输入子系统
    input_subsystem = unreal.get_engine_subsystem(unreal.EnhancedInputSubsystem)
    
    # 为本地玩家添加映射上下文
    local_player = unreal.LocalPlayer.get_local_player()
    if local_player:
        input_subsystem.add_mapping_context(mapping_context, 0)

    return move_forward_action, move_right_action

def bind_input_events(player_controller):
    # 设置输入组件
    enhanced_input = player_controller.get_enhanced_input_component()
    
    # 获取输入动作
    move_forward, move_right = setup_wasd_mappings()
    
    # 绑定输入事件
    enhanced_input.bind_action(
        move_forward,
        unreal.InputTriggerEvent.TRIGGERED,
        lambda ctx: handle_movement(ctx, "Forward")
    )
    
    enhanced_input.bind_action(
        move_right,
        unreal.InputTriggerEvent.TRIGGERED,
        lambda ctx: handle_movement(ctx, "Right")
    )

def handle_movement(context, direction):
    input_value = context.get_value()
    axis_value = input_value.get_magnitude()
    
    if direction == "Forward":
        print(f"前后移动输入值: {axis_value}")  # W=1.0, S=-1.0
    elif direction == "Right":
        print(f"左右移动输入值: {axis_value}")  # D=1.0, A=-1.0
