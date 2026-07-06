from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return HttpResponse("ファイルがありません", status=400)
            
        try:
            df = pd.read_csv(csv_file)
            
            instrument_cols = [
                'ボーカル （ひらがなフルネーム）\\n※ボーカルが他の楽器も兼任する場合はこの欄にのみ記入してください。',
                'バッキングギター （ひらがなフルネーム）',
                'リードギター （ひらがなフルネーム）',
                'ベース （ひらがなフルネーム）',
                'ドラム （ひらがなフルネーム）',
                'キーボード （ひらがなフルネーム）',
                'その他 （ひらがなフルネーム）'
            ]
            
            valid_cols = [col for col in instrument_cols if col in df.columns]
            all_names = []
            
            for index, row in df.iterrows():
                band_members = []
                for col in valid_cols:
                    val = row[col]
                    if pd.notna(val):
                        # スペースを完全に消去
                        name = str(val).replace(' ', '').replace(' ', '').strip()
                        if name:
                            band_members.append(name)
                
                # 1バンド内の重複（ギタボ）を排除
                unique_band_members = list(set(band_members))
                all_names.extend(unique_band_members)
            
            counts = pd.Series(all_names).value_counts()
            
            result_df = pd.DataFrame({
                'name': counts.index,
                'count': counts.values
            })
            
            # 【変更点】出演数に関係なく、名前（name）のあいうえお順（昇順=True）だけでソート
            result_df = result_df.sort_values(by=['name'], ascending=[True])
            
            member_list = result_df.to_dict(orient='records')
            return render(request, 'member/upload.html', {'member_list': member_list})
            
        except Exception as e:
            return HttpResponse(f"エラーが発生しました: {e}", status=500)
            
    return render(request, 'member/upload.html')