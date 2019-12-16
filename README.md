# marvel
知识图谱练手项目，展示漫威宇宙英雄的关系。
## 数据获取
1. 通过[漫威开发者网站](https://developer.marvel.com/docs)提供的数据作为整个项目的基础

2. 通过[marvel](https://pypi.org/project/marvel/)这个库进行相关的数据请求,
具体的请求的参数情况可以参见marvel开发者网站对应的数据接口
```python
 
 m = Marvel(public_key, private_key)
 character = m.characters.get(1011334)
```
3. 首先将数据存放到本地的mongodb数据库中，然后对数据进行进一步的分析处理。
4. 将处理好的数据存到csv文件中，分别为表示节点的node.csv和表示边的edge.csv
5. 本项目的public_key和private_key是通过**userInfo.conf**文件来读取的，内容为如下格式
```python
[key]
private_key = ***
public_key = ***
```
## 数据展示
数据展示主要通过**gephi**进行数据展示
### 1. 打开文件
文件->打开->选择文件->选择要导入的列->导入
需要注意的是有node文件和edge文件。然后edge文件有记得勾选
加入到已经存在的工作空间中
### 2. 布局窗口
选择 Fruchterman Reingold 方式
区参数 80000 ：确定图形大小面积
重力 4 :牵引所有节点靠近中心
点击运行，看到收敛后停止运行
### 3.统计窗口
选择运行**模块化**选项，
这样会在node数据表的基础上添加一列modularity class。
类似于机器学习中的聚类算法，将所有的数据分成几大类。
### 4. 外观选项
1. 节点->颜色（第一个小图标）->partition->选择经过模块化步骤所产生的Modularity Class
2. 节点->大小（第二个小图标）->ranking->选择weight->根据图中显示的调整最小和最大尺寸
3. 节点->标签大小（第四个小图标）->ranking->选择weight->根据图中情况自行调整最小尺寸和最大尺寸。
4. 边也是同样的方式进行调整。我这里选择了默认。
### 5. 图
![]( http://q1tldblw4.bkt.clouddn.com/qiniu_kwimggephi.jpg)
这里重点说一下下面四个框的作用，
1. 在图中是否显示标签
2. 边的宽度
3. 标签的字体和大小，可以自己进行调整
4. 标签的相对大小。
### 6. 预览与保存
### 预览并保存
![]( http://q1tldblw4.bkt.clouddn.com/qiniu_kwimg1576509213541.jpg)

1. 可以通过上面的预览选项来进入预览界面，如果中间没有预览界面，可以依次点击**窗口**->**预览**来调试出来。
2. 注意在预览设置中设置是否显示节点标签，显示边等选项。
3. 同时要注意gephi的中节点标签的显示是和导入的node文件中的**label列**对应的，所以如果如果本身没有设置label标签，那么可以自己添加一列要显示的数据到label列中，依次点击【数据资料】->【点数据】->复制列->复制到label中即可完成操作。
4. 可以根据整个页面中节点数目的疏密程度来设置节点的大小，标签的大小，设置边的宽度等。尽量保持一个比较好的观感。 
5. 左下角有对应的输出，可以保存为svg/pdf/png,可以自行选择

## 结果展示
![]( http://q1tldblw4.bkt.clouddn.com/qiniu_kwimgmarvel.png)

由于数据太多（99个），所以整个的效果图没有想象中的好看，因为是练手项目，所以就先暂时到此为止了。
可以放上参考项目的效果图，他们只展示了25个角色的数据
![]( http://q1tldblw4.bkt.clouddn.com/qiniu_kwimgidealmarvel.jpg)
## 项目参考
[漫威角色关系图](https://gitee.com/crossin/snippet/tree/master/marvel-gephi)
故事数大于等于709的25个角色数据


