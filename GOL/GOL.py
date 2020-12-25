import matplotlib.pyplot as plt
import random


class GOL:
    def __init__(self):
        # initialize
        self.state = 0
        self.total_cell = 0
        self.grid = plt.figure(facecolor='k')
        self.axes = self.grid.add_subplot(111, projection='3d')
        self.axes.set_facecolor('k')
        self.delay_time = 0.3

        # set min and max value for grid
        self.min_value = 0
        self.max_value = 9
        self.axes.set_xlim3d(self.min_value, self.max_value)
        self.axes.set_ylim3d(self.min_value, self.max_value)
        self.axes.set_zlim3d(self.min_value, self.max_value)
        self.axes.xaxis.set_ticklabels([])
        self.axes.yaxis.set_ticklabels([])
        self.axes.zaxis.set_ticklabels([])
        self.axes.xaxis.set_ticks([])
        self.axes.yaxis.set_ticks([])
        self.axes.zaxis.set_ticks([])
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.axes.set_zlabel('z')

        # for swapping of main array
        self.array = []
        self.temp_array = []

        # for filling the white space in grid
        self.default_array_x = []
        self.default_array_y = []
        self.default_array_z = []

        # for plotting cells
        self.array_x = []
        self.array_y = []
        self.array_z = []

        # cell value
        self.cell_rate = 30
        self.cell_size = 60
        self.alive_cell = 'ko'
        self.dead_cell = ''
        self.text_color = 'w'
        self.cell_marker = '.'

        for x in range(self.min_value, self.max_value + 1):
            for y in range(self.min_value, self.max_value + 1):
                for z in range(self.min_value, self.max_value + 1):
                    # random create cell on grid
                    is_true = random.randint(0, 101)
                    if is_true > 100 - self.cell_rate:
                        self.array.append((x, y, z))
                    else:
                        self.array.append(('', '', ''))
                    # create an empty temp array for swapping
                    self.temp_array.append(('', '', ''))
                    self.default_array_x.append(x)
                    self.default_array_y.append(y)
                    self.default_array_z.append(z)

        for x, y, z in self.array:
            if x != '':
                self.total_cell += 1

        self.axes.text2D(-0.09, 0.95, 'Generation: ' + str(self.state), color=self.text_color,
                         transform=self.axes.transAxes)

        self.axes.text2D(0.90, 0.95, 'Total Cell: ' + str(self.total_cell), color=self.text_color,
                         transform=self.axes.transAxes)

        for x, y, z in self.array:
            if x != '':
                self.array_x.append(x)
                self.array_y.append(y)
                self.array_z.append(z)
                # color = (x / (self.max_value + 1), y / (self.max_value + 1), z / (self.max_value + 1))
                # self.axes.scatter(x, y, z, color=color, marker=self.cell_marker, s=self.cell_size)

        # self.axes.plot(self.default_array_x, self.default_array_y, self.default_array_z, self.dead_cell)

        self.axes.plot(self.array_x, self.array_y, self.array_z, self.alive_cell)
        self.array_x = []
        self.array_y = []
        self.array_z = []

        plt.draw()
        plt.pause(self.delay_time)
        self.simulation()

    def new_temp_array(self):
        """
            create an empty temp array for swapping
        """
        for x in range(self.min_value, self.max_value + 1):
            for y in range(self.min_value, self.max_value + 1):
                for z in range(self.min_value, self.max_value + 1):
                    self.temp_array.append(('', '', ''))

    def calc_cell(self):
        """
            rules:
                alive cells with < cell_lower_limit alive neighbor(s) -> dead next gen
                alive cells with cell_lower_limit or cell_upper_limit neighbors-> live next gen
                alive cells with > cell_upper_limit neighbors -> dead next gen
                dead cells with exactly cell_upper_limit neighbors -> live next gen
        """
        total_cells_around = 0
        offset_z = (self.max_value + 1) * (self.max_value + 1)
        offset_y = self.max_value

        cell_lower_limit = 3
        cell_upper_limit = 5

        """
            cell order:
                same z:          before-z:           behind-z:
                    |0|1|2|             |8|9|10|            |17|18|19|
                    |3|x|4|             |11|12|13|          |20|21|22|
                    |5|6|7|             |14|15|16|          |23|24|25|
        """
        for i in range(len(self.array)):
            """
                same z
            """
            # cell 0
            try:
                if self.array[i + offset_y - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 1
            try:
                if self.array[i + offset_y] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 2
            try:
                if self.array[i + offset_y + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 3
            try:
                if self.array[i - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 4
            try:
                if self.array[i + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 5
            try:
                if self.array[i - offset_y - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 6
            try:
                if self.array[i - offset_y] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 7
            try:
                if self.array[i - offset_y + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            """
                before-z
            """
            # cell 8
            try:
                if self.array[i - offset_z + offset_y - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 9
            try:
                if self.array[i - offset_z + offset_y] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 10
            try:
                if self.array[i - offset_z + offset_y + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 11
            try:
                if self.array[i - offset_z - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 12
            try:
                if self.array[i - offset_z] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 13
            try:
                if self.array[i - offset_z + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 14
            try:
                if self.array[i - offset_z - offset_y - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 15
            try:
                if self.array[i - offset_z - offset_y] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 16
            try:
                if self.array[i - offset_z - offset_y + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            """
                behind-z
            """
            # cell 17
            try:
                if self.array[i + offset_z + offset_y - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 18
            try:
                if self.array[i + offset_z + offset_y] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 19
            try:
                if self.array[i + offset_z + offset_y + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 20
            try:
                if self.array[i + offset_z - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 21
            try:
                if self.array[i + offset_z] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 22
            try:
                if self.array[i + offset_z + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 23
            try:
                if self.array[i + offset_z - offset_y - 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 24
            try:
                if self.array[i + offset_z - offset_y] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # cell 25
            try:
                if self.array[i + offset_z - offset_y + 1] != ('', '', ''):
                    total_cells_around += 1
            except IndexError:
                pass

            # print(total_cells_around)

            if total_cells_around == cell_upper_limit and self.array[i] == ('', '', ''):
                """
                    how to find the coordinate of the cell
                    1   (0, 0, 1)   x, y, z
                    3   (0, 0, 3)
                    18  (0, 1, 8) 
                    27  (0, 2, 7)
                    29  (0, 2, 9)
                    44  (0, 4, 4)
                    100 (1, 0, 0)
                """
                # for index, value in enumerate(self.array):
                #     if value != ('', '', ''):
                #         print(index, value)

                if i < 10:
                    x = i
                    y = 0
                    z = 0
                elif 10 <= i < 100:
                    x = str(i)[0]
                    y = str(i)[1]
                    z = 0
                else:
                    x = str(i)[0]
                    y = str(i)[1]
                    z = str(i)[2]
                self.temp_array[i] = (int(x), int(y), int(z))
            elif cell_lower_limit <= total_cells_around <= cell_upper_limit:
                self.temp_array[i] = self.array[i]
            elif total_cells_around < cell_lower_limit or total_cells_around > cell_upper_limit:
                self.temp_array[i] = ('', '', '')

            total_cells_around = 0

        self.array = self.temp_array
        self.temp_array = []
        self.new_temp_array()

    def simulation(self):
        # start simulate
        while self.total_cell > 0:
            self.calc_cell()

            # clear the last grid
            plt.cla()
            self.axes.xaxis.set_ticklabels([])
            self.axes.yaxis.set_ticklabels([])
            self.axes.zaxis.set_ticklabels([])
            self.axes.xaxis.set_ticks([])
            self.axes.yaxis.set_ticks([])
            self.axes.zaxis.set_ticks([])
            self.axes.set_xlabel('x')
            self.axes.set_ylabel('y')
            self.axes.set_zlabel('z')

            # calculate new cells
            self.state += 1
            self.axes.text2D(-0.09, 0.95, 'Generation: ' + str(self.state), color=self.text_color,
                             transform=self.axes.transAxes)

            self.total_cell = 0
            for x, y, z in self.array:
                if x != '':
                    self.total_cell += 1
            self.axes.text2D(0.90, 0.95, 'Total Cell: ' + str(self.total_cell), color=self.text_color,
                             transform=self.axes.transAxes)

            for x, y, z in self.array:
                if x != '':
                    self.array_x.append(x)
                    self.array_y.append(y)
                    self.array_z.append(z)
                    # color = (x / (self.max_value + 1), y / (self.max_value + 1), z / (self.max_value + 1))
                    # self.axes.scatter(x, y, z, color=color, marker=self.cell_marker, s=self.cell_size)

            # self.axes.plot(self.default_array_x, self.default_array_y, self.default_array_z, self.dead_cell)

            self.axes.plot(self.array_x, self.array_y, self.array_z, self.alive_cell)
            self.array_x = []
            self.array_y = []
            self.array_z = []

            # draw new gird
            plt.draw()
            plt.pause(self.delay_time)

        plt.show()
