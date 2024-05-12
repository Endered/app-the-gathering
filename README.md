# app-the-gathering
Nix Package Manager + AppImage + BusyBox Pattern = Super Power

Thank you!!!!
https://github.com/ralismark/nix-appimage

注意: これ以降は一旦日本語で書きます(後で英語に書き直すと思います)


# これはなに
AppImageだとどうしてもファイルサイズが大きくなるという問題点をBusyBox方式でソフトウェアを提供することである程度改善しようというプロジェクトです。
AppImageのビルドには上記に記載したnix-appimageをパッケージの管理にはNix package managerを使用しています。

# 使い方
(example.shに実際に使う時の流れを書いているので参考にしてください)

まずはDockerImageをビルドしてください。
ビルド後にapps.jsonという名前のJSONファイルが入ったディレクトリを/src/以下へボリュームでマウントして実行すると、AppImageをそのディレクトリ以下に生成してくれます(JSONファイルの内容については後述)。
生成されたAppImageは、BusyBoxの様にバイナリに対するソフトリンクを貼って使用します。
また簡単のために`--softlink`を引数として実行すると自動でソフトリンクを貼るようにしているので、そちらを使っても問題ありません。


## JSONの内容について
以下のフォーマットで書いてください

また、どのパッケージが使えるのかについては https://search.nixos.org/packages を参照してください。
```
{
  "dependencies" : {
    "vim" : [ # パッケージの名前
      {
        "binary-name" : "vim" # パッケージに含まれる使用したいバイナリファイルの名前
      }
     ],
     "coreutils" : [
       {
         "binary-name" : "cat",
         "alternate-name" : "corecat" # 通常(cat)と違う名前でコマンドを呼びたいとき
       },
       {
         "binary-name" : "date" # 一つのパッケージから複数のバイナリを使用したいとき
       }
     ],
     "gawk" : [
       {
         "binary-name" : "gawk",
         "alternate-name" : "awk"
       }
    ]
  }
}
```
