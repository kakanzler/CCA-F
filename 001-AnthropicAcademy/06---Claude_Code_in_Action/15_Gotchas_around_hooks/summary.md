# [Gotchas around hooks]()

## Summary

hooksに記述する際のsecurityの観点でのテクニックが示されている。

1. 絶対pathでファイルやフォルダは指定すること
   - *path interception*, *binary planting* のリスクを軽減できる。
2. `settings.example.json`を作成し、そこに`$PWD`を記載してPATHを書き、メンバーに共有すること
   - 絶対パスは自身の環境に依存するようになりがちなため、他者に共有する前提ではPATHが壊れてしまう。そこで`$PWD`としてpathを`settings.example.json`に記載して作成し、例えば、`npm run setup`を実行する際に依存関係を解消させる過程で、`$PWD`がProjectのメンバーの環境に合わせた絶対パスに書き換え、`settings.local.json`を作成できるようなスクリプトを書く方法によって吸収する方法が提案されている。


### Note/Tips



## Supplement

- **path interception** <sup>[1](#ref1), [2](#ref2)</sup>:
  - 日本語では、「実行パスのハイジャック」、「実行ファイルの横取り」、「バイナリ・プランティング（Binary Planting）」と呼ばれることが多いようだ。
  - 概要：
    - path interceptionにはいくつか種類がある。呼び出されるファイルがSUID(SetUserID)、つまりファイル所有者の権限ではなく一時的に実行ユーザーの権限で実行されるバイナリの場合に、
      - 環境変数PATH
        - OSがコマンドをたたく際に参照する環境変数で、Pathがリストになっているやつ。新しいコマンドをインストールしたのにPathを通していないからコマンドをたたけない時に追加する先のいつものあれ。
        - 正当なpathが読まれる前に、悪意のあるpathを割り込ませ、それを読ませる手法。Adversaries(攻撃者)は自身にWRITE権限のあるディレクトリへのpathを`$PATH`を追加し、そこで悪意のあるライブラリを読ませルように仕向ける。
        - MAC OSの場合は `$HOME`, `/etc/paths.d`などを書き換えられてしまう。
      - 検索順序のハイジャック
        - プログラムがほかのプログラムを呼び出す際に相対パスで指定していることがある。その際に、正規の実行ファイルよりも先に検索され、呼び出されるように偽の同盟ファイルを配置し、実行を横取りする方法。
      - DLLハイジャック
        - アプリケーション起動時に読み込まれるDLL(Dynmaic Linker Library)が呼び出される直前に偽のDLLを読み込ませる方法。
- **binary planting** <sup>[3](#ref3)</sup>:
  - AdversariesがLocal or Remote File Systemに悪意のあるファイルやライブラリを設置し、脆弱なSWからそれを読み込ませるように仕向ける攻撃の総称。
    - 信頼できるディレクトリに配置したり、BOXとかのRemote File Systemsに配置する
    - *Insecure Access Permissions-based Attack*
      - WindowsはApplciationを新ストールするとインストーラーが`C:\Application`を作成するが、攻撃者はここに、悪意のあるライブラリ`WINIAPI.DLL`を配置し、他のユーザーがアプリを呼び出すときに一緒に呼び出させ、実行させる手法
    - *Current Working Directory-based Attack*
      - WindowsのApplicationは`LoadLibrary("DWMAPI.DLL")`によって`DWMAPI.DLL`をロードされるケースがあり、特にWindows System32フォルダに配置されていることがあるが、これはWindows Vista,7にしかなく、またApplicationが`.bp`ファイルと関連づいているケースにおいて、攻撃者の管理するネットワークフォルダを作成し、`honeypot.bp`といった悪意のあるファイルを配置させることで、Applicationが呼ばれる際にこのファイルをロードさせる手法

## Reference

<a src="ref1"></a>
１．[【セキュリティ】Privilege Escalation — PATH（環境変数）ハイジャック攻撃まとめ](https://qiita.com/nozomi2025/items/7bf5ef2b5875ec6c8536)

<a src="ref2"></a>
２．[Hijack Execution Flow: Path Interception by PATH Environment Variable](https://attack.mitre.org/techniques/T1574/007/)

<a src="ref3"></a>
３．[Binary Planting](https://owasp.org/www-community/attacks/Binary_planting)
