# B+tree

# 자료구조
Node는    key배열, pointer배열, 그리고   자신의    부모를   가리키는    포인터를    가지는    클래스
Leaf는    Node에게    상속받은    클래스로써    Node가    가지고    있는    variable외에도    이전    leaf와    다음    leaf 를   가리키는    포인터를    가진다.

# Insertion 
키가 위치할 적절한 Leaf를 찾고 해당 Leaf에 key와 value쌍을 집어넣는다. Leaf가 넘치면 leaf를 (n/2  올림)만큼 split하여 오른쪽 리프를 생성 후 부모에 오른쪽 리프의 첫 key와 오른쪽 leaf의 주소를 삽입.  그 위의 Node 또한 넘치면 leaf와 같은 방식으로 split  후 부모에 오른쪽 노드의 첫 키와 주소를 삽입

# Deletion
Leaf에 위치한 키와 value를 삭제, 삭제 이후 Leaf가 최소 수치보다 적다면 오른쪽이나 왼쪽 중 키가 많은 Leaf에서 하나의 key value를 빌려온다. 만약 삭제할 키가 leaf의 첫 키인 경우 상위 노 드 중 삭제할 키를 leaf의 두번째 key로 replace.  만약 왼쪽 오른쪽 둘다 현재 leaf와 합쳐도 키의 최대 개수를 넘지않는 경우, 키가 그나마 많은 쪽과 merge를 진행.  상위 노드 또한 leaf와 같은 메커니즘으로 웬만하면 트리의 구조를 변하게 하는 merge를 안하려고 하는 게으른(?) 트리이다.

# Rangesearch
해당    키를    leaf에서    찾고    end보다    크거나   트리    끝에    도달    시    실행    종료 
# Singlesearch 
해당    키를    루트에서부터   시작하여    Leaf까지    탐색을    하면서    방문한    노드를    출력 

# Internal Structure
Class Node:

def index(key): key보다   큰    item의    인덱스를    반환

def tostring(): node의    key들을   string으로    반환
def isfull(): 키의    개수가   최대   개수를    넘는지   여부    검사
def nodeinsert(key,value): leaf가    아닌    node에    key,value 삽입
def borrow(idx, prevornext): idx 부모의    몇번째    포인터   자신을    가리키고    있는지prevornext: 왼쪽    오른쪽    진행    여부    결정, 왼쪽이나    오른쪽    노드에서    키, pointer쌍    가지고    오고   난 후   부모노드    반환
def merge(idx, prevornext): borrow함수    parameter와    동일    왼쪽이나   오른쪽    노드와    merge 진행    후 부모노드    반환
class Leaf():
def leafinsert(key,value): key value쌍    Leaf에    삽입
def delete(key): Leaf에서    key 삭제
def borrow(prevornext) 왼쪽   오른쪽    중    key개수가   많은    리프로부터    key, value 빌려옴
def merge(prevornext) 왼쪽   오른쪽    key 개수가    많은   리프와    merge
def leafsplit() leaf가    넘칠   때   split
class Bplustree():
def findleaf(key, singlekeysearch=None) 해당키가    위치할    혹은    위치한    leaf 찾기   singlekeysearch일 경우    탐색한    경로의    node의   key들    출력
def replace(replacekey, key): leaf의    키가    삭제될    경우    상위노드에    해당키가    있을    경우    다른    키로 대체
def ismin(node) 해당    node가    최소개수보다   적은지    판별
def rangedsearch(start, end) start end사이   key value쌍   출력
def merge(leaf, prevornext): leaf의    merge에서부터   시작해서    전체적인    merge작업   수행
leaf merge-> node borrow 안되면    merge
def prevornext(node) node의   merge나    borrow 방향    결정   prevornext반환
def borrow(leaf, prevornext) leaf borrow진행
def deletion(key):  트리의    전체적인    삭제작업을    진행    leaf에서    key, value쌍    삭제->  상위노드에서 해당    키    삭제->leaf-borrow         ->node borrow 안되면    merge
-안되면    merge->node borrow 안되면    merge
def treeinsert(key, value)  트리의 전체적인 입력 작업 진행, leafinsert(key, value)-> 넘치는지 여부확인-> split -> 상위    노드에   삽입    -> 상위노드    넘치는지    여부    검사-> 반복
Compile instruction 
반드시    input.csv delete.csv는   소스파일(.py)과    같은    디렉토리(Source)에    있어야   한다. 항상    creation 명령을    먼저, deletion이나    search하기   전에는    insertion을    진행
