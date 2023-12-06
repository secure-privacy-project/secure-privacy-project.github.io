<style>
  body {
    font-family: Meiryo;
  }
</style>

[Japanese](index.md) / [English](index_eng.md)

## 目標

不正侵入によるデータの漏洩, 正当なユーザによるデータの持ち出し, 解析結果からの(故意または過失による)個人の特定, などの懸念を払拭, 軽減する, システムソフトウェア(データ基盤, OS), データ解析(差分プライバシー, 連合学習), 実応用(医療データ, 軌跡データ活用)の研究を一体的に進め, 安全に積極的なデータ活用可能なSociety 5.0の実現に貢献することを目指します.

[本プロジェクト](https://www.jst.go.jp/kisoken/crest/project/1111114/1111114_2021.html) はJST CREST [「基礎理論とシステム基盤技術の融合によるSociety 5.0のための基盤ソフトウェアの創出」](https://www.jst.go.jp/kisoken/crest/research_area/ongoing/bunya2021-2.html) 領域に採択されています.

## 体制

* 代表
 * [田浦健次朗](https://www.eidos.ic.i.u-tokyo.ac.jp/~tau/) 東京大学大学院 [情報理工学系研究科](https://www.i.u-tokyo.ac.jp/) [電子情報学専攻](https://www.i.u-tokyo.ac.jp/edu/course/ice/index.shtml) 
* 主たる研究分担者
 * [吉川正俊](https://www.db.soc.i.kyoto-u.ac.jp/~yoshikawa/) 京都大学大学院 [情報学研究科](https://www.i.kyoto-u.ac.jp/) [社会情報学専攻](https://www.soc.i.kyoto-u.ac.jp/)
 * 花岡昇平 東京大学 [附属病院](https://www.h.u-tokyo.ac.jp/) [放射線科](http://www.ut-radiology.umin.jp/) [画像情報処理解析研究室](http://www.ut-radiology.umin.jp/ical/) [CV](https://1drv.ms/w/s!AsqSQ39DdrGCg-5M5j3wuuh_IyPwPQ?e=1GGkOt)
 * [塙敏博](https://www.cspp.cc.u-tokyo.ac.jp/hanawa/) 東京大学 [情報基盤センター](https://www.itc.u-tokyo.ac.jp/) 
 * [曹洋](https://yangcao88.github.io/) 北海道大学 [情報科学研究院](https://www.ist.hokudai.ac.jp/) [情報理工学部門](https://www.csit.ist.hokudai.ac.jp/)
* 共同研究者
 * 田浦G
   * 姜仁河
   * 建部修見
   * 合田憲人
 * 花岡G
   * 柴田 寿一 - [DP-Glow](https://www.mdpi.com/2076-3417/13/18/10132) 
   * 竹永 智美 - Local differential privacy protection for multi-dimensional medical checkup data: real-world validation (under review)
   * Alam MD Ashraful - Estimation of future occurrence of HbA1c elevation with and without Differential Privacy (under review)
   * 菊地 智博 ＠ 自治医大放射線科 - [Synthetic data generation method for hybrid image-tabular data using two generative adversarial networks.](https://arxiv.org/abs/2308.07573)
   * 野村 行弘 ＠ [千葉大 野村研究室](https://www.cfme.chiba-u.jp/staff/detail.php?index=nomura) - [DPSGD](https://1drv.ms/i/s!AsqSQ39DdrGCjagndybXE2nYbw9F-A?e=f16Qss)
   * 山田 藍樹 ＠ [千葉大 野村研究室](https://www.cfme.chiba-u.jp/staff/detail.php?index=nomura) - Investigation of federated learning for automated cerebral aneurysm detection in head MR angiography images (peresented in CARS 2023)
 * 塙G
   * 中村 遼
   * 空閑 洋平

## 研究内容

![目標](img/goals.png "サンプル")

 * 医用データ(診断画像, 電子カルテ, レセプトデータ), 人や物の位置情報データなど, 有用なデータの多くが個人情報に基づいています
 * それらのデータは通常, 個人の識別に必要な情報は除去(仮名化, ハッシング)された上で提供され, かつ目的としても, 機械学習のモデル構築(例: 大量の正常画像, 病理画像を用いて, 画像診断のモデルを構築する)や, 統計的なデータの計算(例: 期間ごと, 施設ごとの利用者数を算出する)など, 個人情報を露呈しない用途で利用されることがほとんどです
 * そうであっても, 個人情報を元にした解析結果(機械学習モデルや統計データ)と, 個人に対する外部知識を組み合わせて個人の情報を特定しうることが知られており(...), 個人情報を妥当な目的で提供・利用するにあたっての障壁になっています
 * また現在用いられているファイルシステムやクラウドストレージではデータの提供 $=$ データの読み出し権限を与える, ということであり, 読み出されたデータのコピー・流出をシステムによって制御することが困難であり, これもまた, データ提供の障壁となっています
 * これらの問題を解決するためには, 読み出したデータを外部に流出(出力)できないことを保証するシステム, 個人の情報を特定しうる結果を出力できないことを保証するシステムなど新しいシステム技術が必要です
 * それと並立するアプローチとして, データそのものをより匿名化し, 個人情報の復元を不可能にするという方法もあります(K匿名化やローカル差分プライバシなど)が, データの有用性が著しく損なわれるという問題があります
 * 本研究ではこれらの問題を解決するために様々なレイヤ(基盤ソフトウェア, アルゴリズムの枠組み, 実応用)で取り組みます
 * 具体的には以下のモジュールに分解し, 連携して取り組みます(すべて進行中の研究であり, 目標やアプローチの変更がありえます)

 1. 管理者への信頼に依拠しないセキュアファイルシステム 
 1. プライバシー保護を強制・追跡可能なシステム機構
 1. 柔軟なプライバシー保護データ解析・機械学習 
 1. 医療・軌跡データ実応用での実証 

### 管理者への信頼に依拠しないセキュアファイルシステム 

### プライバシー保護を強制・追跡可能なシステム機構

 * このサブテーマでは, 個人情報を特定する解析結果の出力を抑止するためのシステム, --- 具体的にはプログラミング言語処理系 --- について研究する
 * 解析結果から個人情報を特定できないようにするための仕組みとして, (グローバル)差分プライバシーの枠組みを活用する
 * グローバル差分プライバシーの枠組みでは, 解析結果(多数の個人データの平均や和など)に確率的なノイズを加えることにより, 解析結果に対する特定個人の寄与を曖昧にし, 結果として解析結果から個人のデータが導き出されることを防ぐ
 * 目指す言語処理系では,
   * 個人の情報に基づくデータ(ファイルやデータベースからの入力を想定), およびそこから計算によって派生したデータは出力を禁止する,
   * 適切なグローバル差分プライバシー機構を通した(確率的なノイズを加えた)データのみ出力を許可する
   ことによりプライバシー漏洩を防止する

### 柔軟なプライバシー保護データ解析・機械学習 

このサブテーマでは、以下の項目を研究する．

-  **TEEを用いるプライバシー保護型連合学習**

![VLDB23-Olive](img/VLDB23-Olive.png)



連合学習（FL）と信頼実行環境（TEE）を組み合わせることは，プライバシーを保護するFLを実現するための有望なアプローチであり，近年，かなりの学術的注目を集めている．サーバー側でTEEを実装することにより，各ラウンドがサーバーに勾配情報を露出することなく連合学習が進行することを可能にする．これは，特に局所的差分プライバシーを用いるFLのユーティリティの増加に約立つ．しかし，サーバー側TEEの脆弱性を考慮する必要があるが，これはFLの文脈で十分に研究されていない．このサブトピックでは，FLにおけるTEEの脆弱性を分析するためのシステムとアルゴリズムを設計し，TEEを強化するための厳密な防御方法を提案し，プライベートかつ高ユーティリティな連合学習にTEEを活用できるシステムの開発を行う．



- **連合学習におけるプライバシー保護した貢献度の計算**

![vldb23-secSV](img/vldb23-secSV.png)

連合学習には，各クライアントのデータの貢献度を評価することは重要な課題であり，データ市場，説明可能なAI，または悪意のあるクライアントの検出に応用される．特に，シャープレイ値（SV）は，貢献度評価のためのよく使われた指標である．しかし，既存のFLにおけるSV計算方法は，プライバシーに配慮していない．つまり，既存手法は，サーバーがプライバシー保護されていないFLモデルとクライアントのデータにアクセスできると仮定している．したがって，本トピックでは，プライバシー保護されたSV計算の問題について研究する．我々は，Cross-silo FLにおいて，初めて効率的かつプライベートなSV計算プロトコル，SecSV，を提案した．SecSVの特徴は，ハイブリッドプライバシー保護スキームを利用して，テストデータとモデル間の暗号文-暗号文の乗算を避ける．実験では，SecSVが同型暗号を使用するBaselineよりも5.9-18.0倍速いことを示している．

### 医療・軌跡データ実応用での実証 

 1. 医療サブテーマ
  * 医療サブテーマでは、以下の3つの実証を主に行う
  * 医療現場で実用可能な差分プライバシーによるプライバシー保護システムの開発、デプロイ、実使用経験の蓄積
  * 田浦Gとの共働 

![個人情報保護を強制するプログラミング基盤 の 医療への展開](img/TauraHanaoka.png)

ここでは主に、AIを学習する側、特にAI学習に必須である学習データセットのプライバシーを守るため、
田浦Gが開発しているプライバシー強制技術を使った上で、AIをdifferentially private stochastic gradient discent (DPSGD)の枠組みで学習することにより、学習データに使われた患者さんの情報が漏洩しにくいようなAI学習の手法論を確立することが目的です。
  * 塙Gとの共働

![セキュアな医用AIの実臨床](img/HanawaHanaoka.png)

ここでは主に、デプロイ側、つまり学習済みのAIをいかに秘密演算やスーパーコンピュータを使って安全に、スケーラブルに実行し、結果を臨床医や患者さんに届けるかを考え、研究を進めて参ります。

## 論文

 1. Shuyuan Zheng, Yang Cao, Masayuki Yoshikawa. "Secure Shapley Value for Cross-Silo Federated Learning." _Proceedings of the VLDB Endowment._ 2023.
 1. Fumiharu Kato, Yang Cao, Masayuki Yoshikawa. "Olive: Oblivious Federated Learning on Trusted Execution Environment against the Risk of Sparsification." _Proceedings of the VLDB Endowment._ 2023.
 1. Shun Takagi, Fumiharu Kato, Yang Cao, Masatoshi Yoshikawa. "From Bounded to Unbounded: Privacy Amplification via Shuffling with Dummies." _2023 IEEE 36th Computer Security Foundations Symposium (CSF)._ 2023.
 1. Ruixuan Liu, Yang Cao, Yanlin Wang, Lingjuan Lyu, Chen Yun, Chang Hong. "PrivateRec: Differentially Private Model Training and Online Serving for Federated News Recommendation." _KDD '23: Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining._ 2023.
 1. Shun Takagi, Yang Cao, Yasuhito Asano, Masatoshi Yoshikawa. "Geo-Graph-Indistinguishability: Location Privacy on Road Networks with Differential Privacy." _IEICE Transactions on Information and Systems._ 2023.
 1. Chao Tan, Yang Cao, Sheng Li, Masatoshi Yoshikawa. "General or Specific? Investigating Effective Privacy Protection in Federated Learning for Speech Emotion Recognition." _ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)._ 2023.
 1. Shumpei Shiina, Kenjiro Taura. "Itoyori: Reconciling Global Address Space and Global Fork-Join Task Parallelism." _In Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC '23)._ 2023.
 1. Hirobumi Shibata, Shouhei Hanaoka, Yang Cao, Masatoshi Yoshikawa, Tomomi Takenaga, Yukihiro Nomura, Naoto Hayashi, Osamu Abe. "Local Differential Privacy Image Generation Using Flow-Based Deep Generative Models." _Applied sciences._ 2023.
 1. Xiaoyu Li, Yang Cao, Masatoshi Yoshikawa. "Locally Private Streaming Data Release with Shuffling and Subsampling." _2023 IEEE 39th International Conference on Data Engineering Workshops (ICDEW)._ 2023.
 1. Ryota Hiraishi, Masatoshi Yoshikawa, Yang Cao, Sumio Fujita, Hidehito Gomi. "Mechanisms to Address Different Privacy Requirements for Users and Locations." _IEICE Transactions on Information and Systems._ 2023.
 1. Cao Xiao, Yang Cao, Primal Pappachan, Atsuyoshi Nakamura, Masatoshi Yoshikawa. "Differentially Private Streaming Data Release Under Temporal Correlations via Post-processing." _Lecture Notes in Computer Science._ 2023.

