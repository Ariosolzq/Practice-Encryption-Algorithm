# # ascii字符换成数值
# Letter = 'hello world'
# for i in Letter:
#     print(ord(i),end=" ")
#
# # 数值转化为ASCII字符
# list=[104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]
# for i in list:
#     print(chr(i),end="")
# print("\n")

# 代替算法
# 考虑到空格也会被当成一个字符，如果将其识别出来并不加密的话，我认为代替算法的加密性就会受到影响，所以在以下算法中不单独识别空格进行处理
# 修改1：使用模运算来避免字母超出ASCII码的范围
# 处理中文需要更换为Unicode，根据题目要求，以下就可以只使用ASCII码
# 不需要单独考虑Key为负数
def Encrypt_1(Letter,Key):
    list_1 = []
    re_Letter=""
    # 转化为数字并加密，需要使用取模的方法避免Key数值太大的影响
    # 修改：需要保证字符在ASCII码可打印的32到126的范围内
    for i in Letter:
        if 32 <= ord(i) <= 126:
            # 偏移方法：先减32，取余再加回偏移量，确保所有密文都是可以print的
            list_1.append((ord(i) + Key - 32) % 95 + 32)
        else:
            raise ValueError("明文中存在不可打印字符")
    # 解密
    for i in list_1:
        re_Letter += chr(i)
    return re_Letter

def Decrypt_1(Letter,Key):
    list_2 = []
    re_Letter_2 = ""
    # 读取
    for i in Letter:
        list_2.append(ord(i))
    # 反加密+解密
    for i in list_2:
        # 相同的偏移方法：先减32，取余再加回偏移量，确保所有密文都是可以print的
        i = ((i - Key - 32) % 95 + 32)  # 使用模运算处理Key
        if 32 <= i <= 126:
            re_Letter_2 += chr(i)
        else:
            raise ValueError("密文中存在不可打印字符")
    return re_Letter_2

# 换位算法
# 经过测试，以下的换位算法对明文中包含标点符号的情况也能解决
def Encrypt_2(Letter,Key):
    num_count = 0
    list_count = 0
    all_count = 0
    lists = [[]]
    re_Letter = ""

    # 建立二维列表
    for i in Letter:
        # # 如果要单独区分空格的话
        # if i == ' ':
        #   continue
        lists[list_count].append(i)
        num_count += 1
        all_count += 1
        if all_count == len(Letter) and num_count == Key:
            break
        elif num_count == Key:
            list_count += 1
            lists.append([])
            num_count = 0

    # 补充空格
    while num_count < Key:
        lists[list_count].append(" ")
        num_count += 1

    # 删除空列表，防止正好多创建一个列表
    lists = list(filter(None, lists))

    # # 检验列表长度
    # print(len(lists))
    # print(lists)
    # 竖着输出
    for i in range(Key):
        for j in range(len(lists)):
            re_Letter += lists[j][i]

    return re_Letter

def Decrypt_2(Letter,Key):
    num_count = 0
    list_count = 0
    lists = [[]]
    re_Letter = ""
    all_count = 0

    length = int(len(Letter)/Key)
    # print('length:',length)

    # 建立二维列表
    for i in Letter:
        # # 如果要忽略空格的话
        # if i == ' ':
        #   continue
        lists[list_count].append(i)
        num_count += 1
        all_count += 1
        if all_count == len(Letter) and num_count == length:
            break
        if num_count == length:
            list_count += 1
            # if all_count == len(Letter):
            #     break
            lists.append([])
            num_count = 0

    # # 补充空格
    # while num_count < length:
    #     lists[list_count].append(" ")
    #     num_count += 1

    # 删除空列表，防止正好多创建一个列表
    lists = list(filter(None, lists))

    # # 检验列表长度
    # print(len(lists))
    # print(lists)

    # # 去除最后一行的空格，如果最后一个不是空格也会被再次添加回去
    # last_item = lists[len(lists)-1].pop()
    # while last_item == ' ':
    #     last_item = lists[len(lists)-1].pop()
    # lists[len(lists) - 1].append(last_item) # 再次添加

    # print(lists)
    # 竖着输出
    for i in range(length):
        for j in range(Key):
            # print(lists[j][i],end = '')
            re_Letter += lists[j][i]
    # for k in lists[length-1]:  # 单独读取最后一个列表
    #     re_Letter += k
    # 直接删除字符串右侧的空格
    re_Letter = re_Letter.rstrip()
    return re_Letter

# 异或加密算法
# 发现题目中对明文没有限制为英文字母和标点符号等，所以需要对编码格式进行修改，就不能再使用ASCII码了
# def Encrypt_3(Letter,Key):
#     re_letter = ""
#     for i in range(len(Letter)):
#         re_letter += chr(ord(Letter[i])^ord(Key[i]))
#     return re_letter
#
#     list_1 = []
#     re_Letter=""
#     # 转化为数字并加密
#     for i in Letter:
#         list_1.append(ord(i)+Key)
#     # 解密
#     for i in list_1:
#         re_Letter += chr(i)
#
#     return re_Letter
#
# def Decrypt_3(Letter,Key):
#     # 利用异或的特性
#     re_letter = ""
#     for i in range(len(Letter)):
#         re_letter += chr(ord(Letter[i])^ord(Key[i]))
#     return re_letter

def Encrypt_3(Letter,Key):
    import base64

    # 转换为 utf-8 编码的字节序列
    Letter = Letter.encode("utf-8")
    Key = Key.encode("utf-8")

    # 检查 key 的长度，如果Key的长度小于Letter就得重复拼接
    if len(Key) < len(Letter):
        Key *= len(Letter) // len(Key) + 1

    re_letter = ""
    lists = []

    # 异或运算
    for i in range(len(Letter)):
        lists.append(Letter[i] ^ Key[i])

    # 把异或运算的结果转换为字节序列
    lists = bytes(lists)
    # print(lists)

    # 字节序列转化为输出结果
    lists = base64.b64encode(lists).decode("utf-8")
    for i in lists:
        re_letter += i
    return re_letter

def Decrypt_3(Letter,Key):
    import base64

    # 密文解码转化为字节序列
    Letter = base64.b64decode(Letter.encode("utf-8"))
    # 密钥转换为 utf-8 编码的字节序列
    Key = Key.encode("utf-8")

    # 检查 key 的长度，如果Key的长度小于Letter就得重复拼接
    if len(Key) < len(Letter):
        Key *= len(Letter) // len(Key) + 1

    re_letter = ""
    lists = []

    # 异或运算
    for i in range(len(Letter)):
        lists.append(Letter[i] ^ Key[i])

    # 转换为 utf-8 编码的字符串
    lists = bytes(lists).decode("utf-8")
    for i in lists:
        re_letter += i
    return re_letter

# 主函数
if __name__ == '__main__':
    # # 1. 代替算法，为了避免Key太大造成乱码，需要对key进行取模，Key % 256
    # Letter = 'Hello, World!2023{\/ }'
    # Key = 3
    # Letter=Encrypt_1(Letter, Key)
    # print("请去除单引号，以获取加密结果")
    # print("'" + Letter + "'")
    # res = Decrypt_1(Letter, Key)
    # print("请去除单引号，以获取解密结果")
    # print("'" + res + "'")

    # # 2. 换位算法，用数字代替
    # # Letter = "mEEt me after the toga party"
    # Letter = "Hello World"
    # Key = 3
    # if Key >= len(Letter):
    #     print("提示：明文长度小于密钥长度，无法达到理想加密效果")
    #
    # Letter = Encrypt_2(Letter, Key)
    # print("请去除单引号，以获取加密结果")
    # print("'" + Letter + "'")
    # re_Letter = Decrypt_2(Letter, Key)
    # print("请去除单引号，以获取解密结果")
    # print("'" + re_Letter + "'")

    # 3. 异或加密算法，要求Key的长度一定要大于等于Letter的长度
    # 为了解决中文密文乱码的问题，避免使用ASCII码值进行转换，尝试使用UTF-8，并在之后用base64编码进行转换
    import base64
    Letter="Hello World"
    Key= "1"
    # Letter = 3142835701
    # Key = 12345
    Letter = str(Letter)
    Key = str(Key)
    re_letter = Encrypt_3(Letter, Key)
    print("请去除单引号，以获取加密结果")
    print("'" + re_letter + "'")
    Letter = re_letter
    re_letter = Decrypt_3(Letter,Key)
    print("请去除单引号，以获取解密结果")
    print("'" + re_letter + "'")
