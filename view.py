from cui import Cui
import matplotlib.pyplot as plt


class View:
    @staticmethod
    def view_lines_plot(new_sample_df):
        new_sample_df.plot()
        plt.show()

    @staticmethod
    def view_column_plot(new_sample_df):
        new_sample_df.plot(kind='bar')
        plt.show()
