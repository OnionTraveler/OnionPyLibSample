# ===============  以下操作只是為了要可以打印中文字 ===============
# import sys; import codecs; sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach());
# ===============  以上操作只是為了要可以打印中文字 ===============
import os
from datetime import datetime, timedelta
import time

from enum import Enum
class FilenameExtension(Enum):
    log = "log"
    txt = "txt"
    csv = "csv"


class LogTools:
    
    def getAppEntrypointDirectory():
        """
        獲取「主程式進入點的目錄路徑」 (「CWD/app/src/main/python/main.py」這是期待的目錄結構，但沒有Follow也有預設)
        """
        
        CWD = os.getcwd()  # 當前工作目錄(Current Working Directory)路徑
        
        sAppEntrypointDirectory = ""  # 主程式進入點的目錄路徑
        if os.path.isfile(os.path.join(CWD, 'main.py')):  # 「CWD/main.py」檔案若存在
            # print(f"當前工作目錄已有「main.py」則:  (PS. CWD:「{CWD}」)")
            sAppEntrypointDirectory = os.path.join(CWD, '')  # 「CWD/」
        elif (
            os.path.isdir(os.path.join(CWD, '.embenv'))  # 「CWD/.embenv」目錄若存在
        and os.path.isfile(os.path.join(CWD, 'app', 'src', 'main', 'python', 'main.py'))  # 「CWD/app/src/main/python/main.py」檔案若存在
        ):
            # print(f"若「當前工作目錄」是在「方案」下則:  (PS. CWD:「{CWD}」)")
            sAppEntrypointDirectory = os.path.join(CWD, 'app', 'src', 'main', 'python', '')  # 「CWD/app/src/main/python/」
        elif (
            os.path.isdir(os.path.join(CWD, 'src'))  # 「CWD/src」目錄若存在
        and os.path.isdir(os.path.join(CWD, '..', 'app'))  # 「CWD/../app」目錄若存在
        and os.path.isfile(os.path.join(CWD, 'src', 'main', 'python', 'main.py'))  # 「CWD/src/main/python/main.py」檔案若存在
        ):
            # print(f"若「當前工作目錄」是在「app」下則:  (PS. CWD:「{CWD}」)")
            sAppEntrypointDirectory = os.path.join(CWD, 'src', 'main', 'python', '')  # 「CWD/src/main/python/」
        elif (
            os.path.isdir(os.path.join(CWD, 'main'))  # 「CWD/main」目錄若存在
        and os.path.isfile(os.path.join(CWD, 'main', 'python', 'main.py'))  # 「CWD/main/python/main.py」檔案若存在
        ):
            # print(f"若「當前工作目錄」是在「src」下則:  (PS. CWD:「{CWD}」)")
            sAppEntrypointDirectory = os.path.join(CWD, 'main', 'python', '')  # 「CWD/main/python/」
        elif (
            os.path.isdir(os.path.join(CWD, 'python'))  # 「CWD/python」目錄若存在
        and os.path.isfile(os.path.join(CWD, 'python', 'main.py'))  # 「CWD/python/main.py」檔案若存在
        ):
            # print(f"若「當前工作目錄」是在「main」下則:  (PS. CWD:「{CWD}」)")
            sAppEntrypointDirectory = os.path.join(CWD, 'python', '')  # 「CWD/python/」
        else:
            # print(f"其他則將「當前工作目錄」作為「主程式進入點的目錄路徑」  (PS. CWD:「{CWD}」)")
            sAppEntrypointDirectory = os.path.join(CWD, '')
            
        return sAppEntrypointDirectory
        
        
    def WriteLog(Content:str, DirNamePath:str = f"{os.path.join('.', 'log')}", fne:FilenameExtension = FilenameExtension.log):
        """
        寫「Log」的主函式
        """
        
        # 步驟一：檢查目錄路徑字尾，並建立該目錄(若沒有該目錄的話)
        sDirNamePath = DirNamePath.rstrip(os.sep)  # 「os.sep = "\\"」 in Windows & 「os.sep = "/"」 in Linux\
        sAppEntrypointDirectory = LogTools.getAppEntrypointDirectory()
        sDirNameAbsPath = os.path.join(sAppEntrypointDirectory, sDirNamePath[2:]) if (sDirNamePath[0:1] == ".") else sDirNamePath
        if not os.path.isdir(sDirNameAbsPath):
            os.mkdir(sDirNameAbsPath)
        
        # 步驟二：以時間之名確立該LOG檔名，並搭配「步驟一」補足該檔的絕對路徑
        sSysDate = datetime.today().strftime("%Y/%m/%d %H:%M:%S")  # 「sSysDate = DateTime.Now().ToString("yyyy/MM/dd HH:mm:ss");」 in C#
        sFileName = f"{sSysDate[0:10].replace('/', '')}.{fne.value}"
        sFileNamePath = os.path.join(sDirNameAbsPath, sFileName)
        
        # 步驟三：確立LOG裡內文格式(最後加上「\r\n」用以換行)
        sWriteLine = f"{sSysDate} | {Content}" + os.linesep
        
        # 步驟四：寫檔囉!!
        with open(sFileNamePath, 'a', encoding='UTF-8') as f:
            import platform
            if platform.system() == "Windows":  # 判斷作業系統是否為「Windows」
                sWriteLine = sWriteLine.replace('\r\n', '\n')  # 因為「os.linesep」在「Windows」會轉為「\r\n」(在「Linux」會轉為「\n」)，且再用「open(...)」寫檔會把「\n」轉為「\r\n」 --> 故「os.linesep」搭配「Windows」搭配「open(...)」會變成「\r\n\n」，變成會再多一行空格，故在此修正
            f.write(sWriteLine)
        pass
        
        
    def PurgeLog(PurgedayOffset:int = 540, DirNamePath:str = f"{os.path.join('.', 'log')}"):
        """
        清除「Log」的主函式
        """
        
        # 步驟一：檢查目錄路徑字尾，並建立該目錄(若沒有該目錄的話)
        sDirNamePath = DirNamePath.rstrip(os.sep)  # 「os.sep = "\\"」 in Windows & 「os.sep = "/"」 in Linux
        sAppEntrypointDirectory = LogTools.getAppEntrypointDirectory()
        sDirNameAbsPath = os.path.join(sAppEntrypointDirectory, sDirNamePath[2:]) if (sDirNamePath[0:1] == ".") else sDirNamePath
        if not os.path.isdir(sDirNameAbsPath):
            os.mkdir(sDirNameAbsPath)
        
        # 步驟二：獲得並遍歷該目錄下的所有檔案
        for sFileName in os.listdir(sDirNameAbsPath):
            sFileNamePath = os.path.join(sDirNameAbsPath, sFileName)
            if os.path.isfile(sFileNamePath):
                dteLastWriteTime = datetime.strptime(time.ctime(os.path.getmtime(sFileNamePath)), "%a %b %d %H:%M:%S %Y")
                dteDateTimeNow = datetime.today()
                
                # 步驟三：若該檔案的「最後寫入時間」小於指定時辰，就刪除該檔案
                if (dteLastWriteTime < dteDateTimeNow - timedelta(days=PurgedayOffset)):
                    os.remove(sFileNamePath)
        pass

        
    def WriteErrLog4Exception(e:Exception = None, NeedAutoSave:bool = False):
        """
        重構「try ... except Exception as e: ...」之「錯誤訊息內容」，並留Log檔與回傳的主函式
        """
            
        import sys
        import traceback
        
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        
        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)
        
        # Format stacktrace
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f"File:{trace[0]}, Line:{trace[1]}, FuncName:{trace[2]}, Message:{trace[3]}")
        
        errMsg = ""
        errMsg += os.linesep + f"str(e):{str(e)}"  # str(e):division by zero
        errMsg += os.linesep + f"ExceptionType:{ex_type.__name__}"  # ExceptionType:ZeroDivisionError
        errMsg += os.linesep + f"ExceptionMessage:{ex_value}"  # ExceptionMessage:division by zero
        errMsg += os.linesep + f"StackTrace:{stack_trace}"  # StackTrace:['File:main.py, Line:14, FuncName:<module>, Message:onion = 10112222 / 0']
        
        if NeedAutoSave:
            LogTools.WriteLog(errMsg)

        return errMsg


    def SaveSQLToFile(SQL:str, SQLFileName:str):
        """
        將「SQL」文字存入文字檔中的主函式
        """
        
        # 步驟一：建立該指定目錄(若沒有該目錄的話)
        sAppEntrypointDirectory = LogTools.getAppEntrypointDirectory()
        sDirName = r"sSQL"  # 該檔會存在「sSQL」這個目錄名稱下
        
        sDirNameAbsPath = os.path.join(sAppEntrypointDirectory, sDirName)
        if not os.path.isdir(sDirNameAbsPath):
            os.mkdir(sDirNameAbsPath)
        
        # 步驟二：串出該檔的絕對路徑
        sFileNamePath = os.path.join(sDirNameAbsPath, SQLFileName)
        
        # 步驟三：寫檔囉!!
        with open(sFileNamePath, 'w', encoding='UTF-8') as f:
            import platform
            if platform.system() == "Windows":  # 判斷作業系統是否為「Windows」
                sWriteLine = sWriteLine.replace('\r\n', '\n')  # 因為「os.linesep」在「Windows」會轉為「\r\n」(在「Linux」會轉為「\n」)，且再用「open(...)」寫檔會把「\n」轉為「\r\n」 --> 故「os.linesep」搭配「Windows」搭配「open(...)」會變成「\r\n\n」，變成會再多一行空格，故在此修正
            f.write(SQL)
        pass










if __name__ == '__main__':
    # 寫「Log」的範例
    LogTools.WriteLog("=====  PROCESS START =====")
    
    # 清除「Log」的範例
    LogTools.PurgeLog()
    
    # 重構「try ... except Exception as e: ...」之「錯誤訊息內容」，並留Log檔與回傳的範例
    try:
        onion = 10112222 / 0
    except Exception as e:
        errMsg = LogTools.WriteErrLog4Exception(e)
        LogTools.WriteLog(errMsg)
    
    # 將「SQL」文字存入文字檔中的範例
    LogTools.SaveSQLToFile("SELECT sysdate FROM dual", "OnionSQL.sql")

    pass
