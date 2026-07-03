from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def upload_csv(request):
    if request.method == 'POST':
        # 画面から送られてきたファイルを取得
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            return HttpResponse("ファイルがありません", status=400)
            
        # まずはPandasで正しく読み込めるかテスト
        try:
            # DjangoのアップロードファイルをそのままPandasに渡せます
            df = pd.read_csv(csv_file)
            
            # ターミナルにCSVの最初の5行を表示して確認してみる
            print("--- CSVの読み込み成功！ ---")
            print(df.head())
            print("---------------------------")
            
            return HttpResponse("CSVの読み込みに成功しました！ターミナルを確認してください。")
            
        except Exception as e:
            return HttpResponse(f"エラーが発生しました: {e}", status=500)
            
    # GETリクエストのときはアップロード画面を表示する
    return render(request, 'member/upload.html')