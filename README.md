YetAnotherTinyAutomation
========================
YetAnotherTinyAutomation is python programs to automate server operations like Chef, Puppet or juju.  However, work in progress.

Concept
=================
1. Constructed by python programs
2. Easy to install
3. Don't Repeat Ourself.
4. Everything can be automated
5. Small start


Current functions
=================
To install PostgreSQL 9.x on CentOS and Ubuntu

git clone http://github.com/ccat/YetAnotherTinyAutomation
cd ./YetAnotherTinyAutomation/examples
sudo python ./postgrsql_install.py <version>
 * version=9.1/9.2/9.3


To backup PostgreSQL database

git clone http://github.com/ccat/YetAnotherTinyAutomation
cd ./YetAnotherTinyAutomation/examples
sudo python ./postgrsql_backup.py filepath <from gmail address> <to address> <gmail username> <gmail application password>

When filepath includes "%num%", it will be replaced by date.
When "from gmail address" to "gmail application password" are inputted, backup data will be sent.



YetAnotherTinyAutomation 0.01
==================
ChefやPuppet、jujuのような、サーバーの自動化を目的としたPythonプログラムですが、だいぶ作りかけです。



コンセプト
=================
1. Pythonで構成されていること
   ChefがRubyベースなのに対し、YetAnotherTinyAutomationはPythonベースです。
2. インストールが簡単であること
   大がかりなシステムを構築しなくても、単体で動作することを目標とします。
3. Don't Repeat Ourself.
   誰かが苦労したことは出来るだけ組み込み、次の人が同じ苦労をしなくてすむことを目標とします。
4. 構成管理にこだわらず、自動化できることは自動化すること。
   サーバーの設計等についても、自動化できるようなら自動化を試みます。
5. スモールスタートであること
   必要となった機能を必要になったタイミングで追加していきます。


とりあえず出来ること
=================
PostgreSQL 9をCentOSかUbuntuへインストール

git clone http://github.com/ccat/YetAnotherTinyAutomation
cd ./YetAnotherTinyAutomation/examples
sudo python ./postgrsql_install.py <version>
 * version=9.1/9.2/9.3


PostgreSQLをバックアップ

git clone http://github.com/ccat/YetAnotherTinyAutomation
cd ./YetAnotherTinyAutomation/examples
sudo python ./postgrsql_backup.py filepath <from gmail address> <to address> <gmail username> <gmail application password>

filepathに「%num%」が含まれていた場合、日付に置換されます。
gmail関係のオプションが入力された場合、バックアップデータはメール添付で送信されます。

