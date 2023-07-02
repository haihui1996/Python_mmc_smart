import mmc_smart
import pandas as pd
import tkinter as tk
from tkinter import filedialog



def show_message(message):
    """
    Display a message in a pop-up window.

    Args:
        message (str): The message to be displayed.
    """
    # Create the root window
    root_msg = tk.Tk()
    root_msg.title("异常信息")

    def close_window():
        # Close the window and quit the application
        root_msg.quit()

    # Create a label with the message
    label = tk.Label(root_msg, text=message, padx=10, pady=10)
    label.pack()

    # Bind the close window event to the root window
    root_msg.protocol("WM_DELETE_WINDOW", close_window)

    # Start the main event loop
    root_msg.mainloop()


if __name__ == "__main__":
    # 创建Tkinter根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏根窗口

    # 打开文件选择对话框
    file_paths = filedialog.askopenfilenames(filetypes=[('bin files', '*.bin;*.Bin')], title="请选择要解析的bin文件")
    if (not file_paths):
        show_message("未选中文件")
        exit(1)

    mmc_smart_list = []
    # 读取二进制文件
    for filename in file_paths:
        with open(filename, "rb") as file:
            # 读取二进制数据
            data = file.read()
            if len(data) != 1024:
                print(filename, "文件长度错误:", len(data))
                show_message(filename + "文件长度错误")
                exit(1)

            # 解析二进制数据为结构体
            health_report = mmc_smart.sOWN_HealthReport.from_buffer_copy(data)

            # 检查数据合法性
            if (health_report.u16EndTag != mmc_smart.__HEALTH_TAG__) or (health_report.sFTLStatistics.u32FTL_StaTAG != mmc_smart.__FTL_Statistics_TAG__):
                print(filename, "Tag Error:", hex(health_report.u16EndTag))
                show_message(filename + " Tag Error")
                exit(1)

            mmc_smart_list.append(pd.Series(health_report.smart_info_decode()))

    df = pd.DataFrame(mmc_smart_list).transpose()
    output_xlsx = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[('Excel Files', '*.xlsx')],
                                               title="excel文件另存为")
    if (not output_xlsx):
        show_message("输出文件未选中")
        exit(1)
    else:
        df.to_excel(output_xlsx, index=True, sheet_name='SmartInfo')
