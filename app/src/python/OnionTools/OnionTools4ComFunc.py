"""
    **「VS Code」用「Debug Mode」跑：
        1.可以用「"cwd": "${workspaceFolder}/app"」改變「執行時的工作路徑」
        2.可以用「"args": ["ENV=PROD", "DURATION_TYPE=AUTO"]」來加入「執行時的命令行參數列」
        3.範例如下： (./vscode/launch.json)
            {
                // 使用 IntelliSense 以得知可用的屬性。
                // 暫留以檢視現有屬性的描述。
                // 如需詳細資訊，請瀏覽: https://go.microsoft.com/fwlink/?linkid=830387
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "Python: Current File",
                        "type": "python",
                        "request": "launch",
                        "program": "${file}",
                        "console": "integratedTerminal",
                        "justMyCode": true,
                        "cwd": "${workspaceFolder}/app",
                        "args": ["ENV=PROD", "DURATION_TYPE=AUTO"]
                    }
                ]
            }        
"""





import sys

class ComFuncTools:
    class CmdTools:
        
        def __parseDashArgv(Input:list) -> list:  # 只是將輸入的串列若有「['--XXX', 'OOO']」元素，轉換成「['XXX=OOO']」 (只是為了「命令行串列」而設計的功能而已)
            lstResult = []
            
            # 判斷有哪些位置含有「--」這個開頭，將該位置(index)記錄到「lstHashDashIndex」
            lstHashDashIndex = []
            for i in range(len(Input)):
                if (Input[i][:2] == '--') and (i+1 != len(Input)):
                    lstHashDashIndex.append(i)
            
            # 若有在「lstHashDashIndex」裡的元素，將其與臨兵一併處理，其他則不處理
            for i in range(len(Input)):
                if i in lstHashDashIndex:
                    # print("表示遍歷到含有「--」的元素，與其下一個元素一起動作")
                    lstResult.append(f'{Input[i][2:]}={Input[i+1]}')
                elif i in map(lambda x: x+1, lstHashDashIndex):
                    # print("表示遍歷到含有「--」的下一個元素，不需要動作可以略過")
                    pass
                else:
                    # print("表示遍歷到一般元素，直接動作")
                    lstResult.append(Input[i])
            
            return lstResult
        

        def getEnvSysArgvWithParsing() -> list:
            """
            直接抓取「.py」後面的參數並做一個雙橫槓的轉換，行成一個「串列(list)」
            """
            
            lstRowData4EnvSysArgv = sys.argv[1:]
            return ComFuncTools.CmdTools.__parseDashArgv(lstRowData4EnvSysArgv)
        

        def getEnvSysArgv():
            """
            原汁原味的呈現「命令行參數」內容
            """
            return sys.argv[1:]
        
        
        def __cvtKeyValueToDict4List(Input:list) -> list:  # 只是將「['XXX=OOO']」轉換成「{'XXX': 'OOO'}」 (只是為了「命令行串列」而設計的功能而已)
            lstResult = []
            for sElement in Input:
                if "=" in sElement:
                    sKey = sElement[:sElement.find("=")]
                    sValue = sElement[sElement.find("=")+1:]
                    lstResult.append({sKey:sValue})
                else:
                    lstResult.append(sElement)
            
            return lstResult
        
        
        def getEnvSysArgvByKey(Key:str) -> str:
            """
            直接抓取「.py」後面的參數並輸入一個鍵(KEY)取值(VALUE)
            PS. 命令行參數列鍵值對的寫法：「ENV=PROD」或「--ENV PROD」
            """
            
            lstEnvSysArgv = ComFuncTools.CmdTools.getEnvSysArgvWithParsing()
            lstEnvSysArgvAfterCvt = ComFuncTools.CmdTools.__cvtKeyValueToDict4List(lstEnvSysArgv)
            
            for e in lstEnvSysArgvAfterCvt:
                if type(e) is dict:
                    if Key in e:
                        return e[Key]
            
            # 都沒有找到任何相符的KEY，則回傳None
            return None
            
        pass





    class DecodeTools:
        def RemoveNonASCII(Input:str) -> str:
            """
            移除疑難雜症的字元(非ASCII)，不然到時候會因為沒辦法「CP950」或「UTF-8」編碼而報錯
            """
            
            import re
            return re.sub(r'[^\x00-\x7f]+', r'', Input).replace('\x005', '').replace('\x7f', '').replace('\x07', '')
        pass










if __name__ == '__main__':
    # 若參數命令行如下：「python3 src/main/python/main.py 111 222 333 ENV=PROD --Fish Onion HIHI=666」
    from OnionTools.OnionTools4ComFunc import ComFuncTools
    print(ComFuncTools.CmdTools.getEnvSysArgv())  # ['111', '222', '333', 'ENV=PROD', '--Fish', 'Onion', 'HIHI=666']
    print(ComFuncTools.CmdTools.getEnvSysArgvWithParsing())  # ['111', '222', '333', 'ENV=PROD', 'Fish=Onion', 'HIHI=666']
    print(ComFuncTools.CmdTools.getEnvSysArgvByKey('ENV'))  # PROD
    
    print(ComFuncTools.DecodeTools.RemoveNonASCII("說你　好 HIHI"))
    pass
