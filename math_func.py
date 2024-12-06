

class Math_func:
    #"класс содержащий методы для произведения математических расчетов согласно требованиям задания"

    razmer_1_sp1 = []#переменные класса для разделения списка с количеством деталей для каждого способа обработки
    razmer_1_sp2 = []
    razmer_1_sp3 = []
    razmer_2_sp1 = []
    razmer_2_sp2 = []


    answer = []


    def __init__(self, list_num, list_equipment):
        self.list_num = list_num #список для деталей
        self.list_equipment = list_equipment # список количества комплектов
        Math_func.razmer_1_sp1.clear()  # очищаю переменные при запуске нового запроса
        Math_func.razmer_1_sp2.clear()
        Math_func.razmer_1_sp3.clear()
        Math_func.razmer_2_sp1.clear()
        Math_func.razmer_2_sp2.clear()
        Math_func.answer.clear()



    def calculate(self): #метод считающий максимальное количество деталей
        Math_func.filling_list(self)
        Math_func.multi_details(self)
        answer_str, max_num = Math_func.max_sets(self)
        return answer_str, max_num

    def how_much(self):#метод считающий количество деталей изготовленных 1 способом из 2 размера
        Math_func.filling_list(self)
        Math_func.multi_details(self)
        #sum = self.razmer_2_sp1[0] + self.razmer_2_sp1[1] + self.razmer_2_sp1[2]
        return self.razmer_2_sp1

    def multi_details(self): #умножаем готовые детали на колличество листов
        for num in range(0, 3):
            self.razmer_1_sp1[num] = self.razmer_1_sp1[num] * 500
            self.razmer_1_sp2[num] = self.razmer_1_sp2[num] * 500
            self.razmer_1_sp3[num] = self.razmer_1_sp3[num] * 500
            self.razmer_2_sp1[num] = self.razmer_2_sp1[num] * 300
            self.razmer_2_sp2[num] = self.razmer_2_sp2[num] * 300


    def filling_list(self):#распределяю детали по спискам согластно размеров и способов раскроя
        self.razmer_1_sp1.append(self.list_num[0])
        self.razmer_1_sp1.append(self.list_num[5])
        self.razmer_1_sp1.append(self.list_num[10])

        self.razmer_1_sp2.append(self.list_num[1])
        self.razmer_1_sp2.append(self.list_num[6])
        self.razmer_1_sp2.append(self.list_num[11])

        self.razmer_1_sp3.append(self.list_num[2])
        self.razmer_1_sp3.append(self.list_num[7])
        self.razmer_1_sp3.append(self.list_num[12])

        self.razmer_2_sp1.append(self.list_num[3])
        self.razmer_2_sp1.append(self.list_num[8])
        self.razmer_2_sp1.append(self.list_num[13])

        self.razmer_2_sp2.append(self.list_num[4])
        self.razmer_2_sp2.append(self.list_num[9])
        self.razmer_2_sp2.append(self.list_num[14])



    def max_sets(self):
        x = self.razmer_1_sp1
        y = self.razmer_2_sp1
        xy0 = "Размер 1 - раскрой 1, размер 2 - раскрой 1 "
        self.answer.append(xy0)
        res =  [[0] * 3 for i in range(6)]
        for ind in range(6):
            if ind == 5:
                x = self.razmer_1_sp3
                y = self.razmer_2_sp2
                xy5 = "Размер 1 - раскрой 3, размер 2 - раскрой 2 "
                self.answer.append(xy5)
            if ind == 4:
                x = self.razmer_1_sp2
                y = self.razmer_2_sp2
                xy4 = "Размер 1 - раскрой 2, размер 2 - раскрой 2 "
                self.answer.append(xy4)
            if ind == 3:
                x = self.razmer_1_sp1
                y = self.razmer_2_sp2
                xy3 = "Размер 1 - раскрой 1, размер 2 - раскрой 2 "
                self.answer.append(xy3)
            if ind == 1:
                x = self.razmer_1_sp2
                xy1 = "Размер 1 - раскрой 2, размер 2 - раскрой 1 "
                self.answer.append(xy1)
            if ind == 2:
                x = self.razmer_1_sp3
                xy2 = "Размер 1 - раскрой 3, размер 2 - раскрой 1 "
                self.answer.append(xy2)

            k1 = ((x[0] + y[0]) / self.list_equipment[0]) - 0.4
            k2 = ((x[1] + y[1]) / self.list_equipment[1]) - 0.4
            k3 = ((x[2] + y[2]) / self.list_equipment[2]) - 0.4

            res[ind][0] = round(k1)
            res[ind][1] = round(k2)
            res[ind][2] = round(k3)

        max_num = min(res[0])
        count = 0
        for num in range(1, 5):
            temp = min(res[num])
            if temp > max_num:
                max_num = temp
                count = num

        ans = f'Лучшее сочетание {self.answer[count]}'
        max_num = min(res[count])
        print(ans)
        return ans, max_num

    def __del__(self):
        class_name = self.__class__.__name__


