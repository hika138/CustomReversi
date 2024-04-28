import os
import random
import numpy as np

gamemode = 0    #0:通常のリバーシ、1:トーラスリバーシ、2:シフトリバーシ
cp = False      #コンピュータ戦モード
turn = 0        #ゲームのターン
boardWidth = 8  #ボードの横幅
boardHeight = 8 #ボードの縦幅
shift_cycle = 2 #盤面を移動させるサイクル
event = 0      #起きた出来事 -1:ゲーム終了 0:何もなし、1:パス、2:盤面の移動

O_disc = 0  #先手の石の数
X_disc = 0  #後手の石の数


#手番は1がO、-1がX
def main():
    global turn
    global gamemode

    while True:
        os.system("cls")
        print("ゲームモードは？")
        print("0:通常リバーシ")
        print("1:トーラスリバーシ")
        print("2:シフトリバーシ")
        gamemode = input(">>")
        if gamemode.isnumeric():
            gamemode = int(gamemode)
            break
    
    os.system("cls")
    turn = 0
    #初期ボードの作成
    cell = np.array([[0] * boardWidth] * boardHeight)
    cell[int(boardWidth/2)][int(boardHeight/2)] = 1
    cell[int((boardWidth/2)-1)][int((boardHeight/2)-1)] = 1
    cell[int(boardWidth/2-1)][int(boardHeight/2)] = -1
    cell[int((boardWidth/2))][int((boardHeight/2)-1)] = -1

    while (True):
        if (is_finish(cell) or event == -1):
            break
        draw_board(cell, event)
        if ((cp == True) and (turn%2 == 1)):
            auto_input(cell)
            input()
        else:
            make_move(cell)
        turn = turn + 1

        if ((turn % shift_cycle) == 0 and gamemode == 2):
            draw_board(cell, 0)
            input("盤面が移動します。")
            shift_cell(cell,random.randint(0, 3))  #上下左右のランダムな方向に移動させる

    count_stones(cell)
    draw_board(cell, event)

#コンピュータ戦の処理
def auto_input(cell):
    global event
    if (turn%2==0):
        print("Oのターン")
        turn_player = 1
    else:
        print("Xのターン")
        turn_player = -1

    for k in range(0, boardHeight*boardWidth*2):
        i = random.randint(0, boardWidth-1)
        j = random.randint(0, boardHeight-1)
        if (is_valid_move(cell, i, j, turn_player)):
            place_and_flip(cell, i, j, turn_player)
            return
    event = 1


#盤面を一つずらす関数
def shift_cell(cell,shift_dir): #shift_cdirは左が0、右が1、上が2、下が3
    global event
    temp = np.array([0]*boardHeight)
    event = 2
    if (shift_dir == 0):    #左
        for i in range(boardHeight):
            temp[i] = cell[0][i]
        for i in range(boardWidth):
            for j in range(boardHeight):
                if not(i == boardWidth-1):
                    cell[i][j] = cell[i+1][j]
                else:
                    cell[boardWidth-1][j] = temp[j]

    elif(shift_dir == 1):   #右
        for i in range(boardHeight):
            temp[i] = cell[boardWidth-1][i]
        for i in range(boardWidth):
            for j in range(boardHeight):
                if not(i == boardWidth-1):
                    cell[boardWidth-1-i][j] = cell[(boardWidth-1-i)-1][j]
                else:
                    cell[0][j] = temp[j]

    elif(shift_dir == 2):   #上
        for i in range(boardWidth):
            temp[i] = cell[i][0]
        for i in range(boardHeight):
            for j in range(boardWidth):
                if not(i == boardHeight-1):
                    cell[j][i] = cell[j][i+1]
                else:
                    cell[j][boardHeight-1] = temp[j]

    elif(shift_dir == 3):   #下
        for i in range(boardWidth):
            temp[i] = cell[i][boardHeight-1]
        for i in range(boardHeight):
            for j in range(boardWidth):
                if not(i == boardHeight-1):
                    cell[j][boardWidth-1-i] = cell[j][(boardWidth-1-i)-1]
                else:
                    cell[j][0] = temp[j]
    return


def count_stones(cell):
    global O_disc
    global X_disc
    for i in range(boardWidth):
        for j in range(boardHeight):
            if cell[i][j] == 1:
                O_disc = O_disc + 1
            elif cell[i][j] == -1:
                X_disc = X_disc + 1
    return


#勝敗の判定
def is_finish(cell):
    global event
    global O_disc
    global X_disc

    O_disc = 0
    X_disc = 0
    for i in range(boardWidth):
        for j in range(boardHeight):
            if cell[i][j] == 0:
                return False
    event = -1
    return True


#入力された手が合法か確認する
def is_valid_move(cell, x, y, turn_player):
    if not(0 <= x < boardWidth and 0 <= y < boardHeight):
        return False
    # 既に駒が置かれている場合は不正な手として扱う
    if cell[x][y] != 0:
        return False
    # 8方向に対して探索を行う
    for i in range(-1, 2):
        count = 0
        for j in range(-1, 2):
            # 位置をずらしながら、同じ色の駒が出てくるまで探索する
            r, c = x + i, y + j
            if gamemode == 1:
                r = r % boardWidth
                c = c % boardHeight
            while (0 <= r < boardWidth) and (0 <= c < boardHeight) and (cell[r][c] == -turn_player):
                count = count + 1
                r, c = r + i, c + j
                if gamemode == 1:
                    r = r % boardWidth
                    c = c % boardHeight
                # 探索中に同じ色の駒が出た場合は、それまでの間に相手の駒があったということなので、この方向に置けることになる
                if  (0 <= r < boardWidth) and (0 <= c < boardHeight) and (cell[r][c] == turn_player):
                    return True
    # どの方向にも置けなかった場合は不正な手として扱う
    return False


#入力された手の処理
def place_and_flip(cell, x, y, turn_player):    
    # 8方向に対して探索を行う
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = x + i, y + j
            if gamemode == 1:
                r = r % boardWidth
                c = c % boardHeight
            flip_list = []
            while 0 <= r < boardWidth and 0 <= c < boardHeight and cell[r][c] == -turn_player:
                flip_list.append((r, c))
                r, c = r + i, c + j
                if gamemode == 1:
                    r = r % boardWidth
                    c = c % boardHeight
            if 0 <= r < boardWidth and 0 <= c < boardHeight and cell[r][c] == turn_player:
                for r_flip, c_flip in flip_list:
                    cell[r_flip][c_flip] = turn_player

    cell[x][y] = turn_player
    return


#手番の処理をする関数
def make_move(cell):
    global event
    #どちらのターンか判定
    if (turn%2==0):
        print("Oのターン")
        turn_player = 1
    else:
        print("Xのターン")
        turn_player = -1
    while(True):
        #駒の設置
        move_str=input("どこに置く？\n>>")
        if move_str == "pass":
            event = 1
            return
        if move_str == "exit":
            event = -1
            return
        move_list = move_str.split(',')
        if len(move_list) ==2 : #入力が"n,m"の形か確認
            x, y = move_list
            if x.isnumeric() and y.isnumeric(): #入力が数値か確認
                    x=int(x.strip())
                    y=int(y.strip())
                    
                    if (is_valid_move(cell, x, y, turn_player)):
                        place_and_flip(cell, x, y, turn_player)
                        return


#ボードを描画する関数
def draw_board(cell, Event):
    global event
    os.system('cls')
    print("TURN:", turn, end="   ")

    if Event == 1:
        print("パスしました。")
    elif Event == 2:
        print("盤面が移動しました。")
    elif Event == -1:
        print("ゲームが終了しました。",end=" ")
        print("Oの石:",O_disc, " Xの石:",X_disc)
    else:
        print("")
    event = 0

    print(" ", end=' ')
    for j in range(boardWidth):
        print(j%10, end=' ')
    print()
    for i in range(boardHeight):
        print(i%10, end=' ')
        for j in range(boardWidth):
            if cell[j][i] == 1:
                print("O", end=' ')
            elif cell[j][i] == -1:
                print("X", end=' ')
            else:
                print('-', end=' ')
        print()


if __name__=="__main__":
    main()