import unreal
import random

# 常量定义
GRID_SIZE = 100  # 网格单位（Unreal单位）
GAME_SPEED = 0.3  # 移动间隔（秒）

subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world = subsystem.get_game_world()
print(world)

subsystem.spawn_actor(unreal.StaticMeshActor.static_class(), unreal.FVector(0, 0, 50), unreal.FRotator(0, 0, 0))  # 在世界中生成一个静态网格Actor
player_controller = unreal.GameplayStatics.get_player_character(world, 0)  # 获取第一个玩家角色
print(player_controller)

class SnakeBody:
    def __init__(self, world, location):
        """创建蛇身段Actor"""
        
        # 加载蓝图类（需提前创建蓝图）
        self.blueprint_class = unreal.load_class(None, "/Game/Objects/BP_Snake_Head.BP_Snake_Head_C")
        print(self.blueprint_class)
        # 生成 Actor
        rotation = unreal.FRotator(0, 0, 0)
        self.actor = unreal.new_object(self.blueprint_class, None, unreal.Name("SnakeHead"))

        self.actor.set_actor_scale3d(unreal.FVector(0.8, 0.8, 0.2))  # 扁平化处理
        self.actor.set_actor_rotation(rotation)  # 设置初始旋转

    def destroy(self):
        """销毁蛇身段"""
        if self.actor :#and self.actor.is_valid():
            self.actor.destroy_actor()  # 使用 destroy_actor 方法销毁 Actor

class SnakeGame:
    def __init__(self):
        # 获取游戏世界
        self.blueprint_class = unreal.load_class(None, "/Game/Objects/BP_Snake_Body.BP_Snake_Body_C")
        # 初始化蛇
        start_pos = unreal.FVector(0, 0, 50)
        self.snake = [SnakeBody(self.world, start_pos)]
        self.direction = unreal.Vector(GRID_SIZE, 0, 0)  # 初始向右移动
        
        # 生成第一个食物
        self.food_actor = None
        self.spawn_food()
        
        # 设置定时器
        self.timer_handle = None
        self.setup_timer()

    def spawn_food(self):
        """在随机位置生成食物"""
        # 销毁旧食物
        if self.food_actor:
            self.food_actor.destroy_actor()  # 使用 destroy_actor 方法销毁 Actor
        
        # 计算有效位置（避开蛇身）
        valid_positions = [
            unreal.FVector(x, y, 50)
            for x in range(-500, 501, GRID_SIZE)
            for y in range(-500, 501, GRID_SIZE)
            if unreal.FVector(x, y, 0) not in [body.actor.get_actor_location() for body in self.snake]
        ]
        
        if valid_positions:
            food_pos = random.choice(valid_positions)
            #self.food_actor = self.world.spawn_actor(unreal.StaticMeshActor.static_class(), food_pos)
            
            # 生成 Actor
            rotation = unreal.FRotator(0, 0, 0)
            self.food_actor = unreal.new_object(self.blueprint_class, None, unreal.Name("SnakeBody"))
            self.food_actor.set_actor_scale3d(unreal.FVector(0.6, 0.6, 0.6))
            self.food_actor.set_actor_location(food_pos, True, False)
            self.food_actor.set_actor_rotation(rotation)  # 设置初始旋转

    def move_snake(self):
        """移动贪吃蛇"""
        if not self.snake:
            return

        # 计算新头部位置
        head_pos = self.snake[0].actor.get_actor_location()
        new_head_pos = head_pos + self.direction
        
        # 检查碰撞
        if self.check_collision(new_head_pos):
            self.game_over()
            return
        
        # 创建新头部
        new_head = SnakeBody(self.world, new_head_pos)
        self.snake.insert(0, new_head)
        
        # 检查食物碰撞
        if self.food_actor and new_head_pos.equals(self.food_actor.get_actor_location()):#, 50):
            self.spawn_food()  # 吃到食物，生成新食物
        else:
            # 未吃到食物，移除尾部
            if len(self.snake) > 1:
                self.snake[-1].destroy()
                self.snake.pop()

    def check_collision(self, position):
        """检测碰撞：边界或自身"""
        # 边界检查（500x500 区域）
        if abs(position.x) > 500 or abs(position.y) > 500:
            return True
        
        # 自身碰撞检查
        for segment in self.snake:
            if position.equals(segment.actor.get_actor_location()):#, 10):
                return True
                
        return False

    def change_direction(self, new_direction):
        """改变移动方向（防止180度转向）"""
        if not self.direction.equals(new_direction * -1, 0.1):
            self.direction = new_direction

    def setup_timer(self):
        """设置游戏定时器"""
        self.timer_handle = unreal.register_slate_post_tick_callback(self.on_tick)

    def on_tick(self, delta_time):
        """引擎每帧调用的核心逻辑"""
        # 通过累积时间控制游戏速度
        if not hasattr(self, 'accumulator'):
            self.accumulator = 0.0
            
        self.accumulator += delta_time
        if self.accumulator >= GAME_SPEED:
            self.accumulator = 0
            self.move_snake()

    def game_over(self):
        """游戏结束处理"""
        unreal.unregister_slate_post_tick_callback(self.timer_handle)
        unreal.log("Game Over! Final length: {}".format(len(self.snake)))
        
        # 清除所有Actor
        for segment in self.snake:
            segment.destroy()
        if self.food_actor:
            #unreal.SystemLibrary.destroy_actor(self.food_actor)
            self.food_actor.destroy_actor()  # 使用 destroy_actor 方法销毁 Actor

def setup_wasd_mappings():
    # 创建输入动作(Input Actions)
    move_forward_action = unreal.InputAction()
    move_forward_action.set_editor_property("ValueType", unreal.InputActionValueType.AXIS1D)
    
    move_right_action = unreal.InputAction()
    move_right_action.set_editor_property("ValueType", unreal.InputActionValueType.AXIS1D)

    # 创建输入映射上下文(Input Mapping Context)
    mapping_context = unreal.InputMappingContext()
    
    # 绑定WASD到对应动作
    mapping_context.map_key(move_forward_action, unreal.FKey("W"))  # 前进 W
    mapping_context.map_key(move_forward_action, unreal.FKey("S"))  # 后退(自动取负值) S
    mapping_context.map_key(move_right_action, unreal.FKey("D"))    # 右移 D
    mapping_context.map_key(move_right_action, unreal.FKey("A"))    # 左移(自动取负值) A

    # 获取增强输入子系统
    input_subsystem = unreal.get_engine_subsystem(unreal.EnhancedInputSubsystem)
    
    # 为本地玩家添加映射上下文
    local_player = unreal.LocalPlayer.get_local_player()
    if local_player:
        input_subsystem.add_mapping_context(mapping_context, 0)

    return move_forward_action, move_right_action 

def bind_input_events():
    move_action = unreal.load_class(None, "/Game/Inputs/IA_Move")
    # 设置输入组件
    enhanced_input = unreal.EnhancedPlayerInput
    
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
    
    #add_key_mapping(87, unreal.Vector(0, -GRID_SIZE, 0))   # 上
    #add_key_mapping(83, unreal.Vector(0, GRID_SIZE, 0))     # 下
    #add_key_mapping(65, unreal.Vector(-GRID_SIZE, 0, 0))    # 左
    #add_key_mapping(68, unreal.Vector(GRID_SIZE, 0, 0))     # 右
    if direction == "Forward":
        print(f"前后移动输入值: {axis_value}")  # W=1.0, S=-1.0
        direction_vector = unreal.Vector(0, -GRID_SIZE * axis_value, 0)
    elif direction == "Right":
        print(f"左右移动输入值: {axis_value}")  # D=1.0, A=-1.0
        direction_vector = unreal.Vector(GRID_SIZE * axis_value, 0, 0)
    
    if snake_game:
        snake_game.change_direction(direction_vector)

# 启动游戏
snake_game = SnakeGame()
bind_input_events()