# Get to Know Your Data

- Data sets are made up of data objects.
- A collection of attributes describes a data object.
- An attribute is a property or characteristic of an object.

- A measurement scale is a rule that associates a value with an attribute of an object.

最后一句话意味测量标度是将数据点的某个属性与一个值关联起来的方法

### **特征的类别**

- Quantitative vs. Qualitative 可量化的与不可量化的，准确的来说是可测量的和不可测量的。注意，并不是标量都是可测量的。**譬如 IP 地址实际上不是可测量的，而是人为约定的。**
- Discrete vs. Continuous 离散与连续：离散特征具有有限个可能或者可数无穷个可能，连续特征在任意两个值之间还有无数个值，譬如温度和海拔。

- 不可量化特征一定是离散的，可量化特征可能是离散的，也可能是连续的

---

- **Nominal or Ordinal 无序和有序**，后者存在具有实际意义的顺序意义。所有的不可量化特征要么是有序的，要么是无序的。binary attributes 二分属性是无序的。A binary attribute is **a nominal attribute with only two categories or states: 0 or 1**, where 0 typically means that the attribute is absent, and 1 means that it is present. 课件上的例子：Nominal attributes (binary attributes) Marriage status, eye color, **Customer ID**
- Interval or Ratio 距离和比率。前者不存在真实的零点，**除法没有实际意义**，譬如摄氏温度。后者存在实际的零点，除法具有实际意义，譬如体重。除法意味着“增长了 5%”这样的语句是有意义的。对于二者最好的区别是考虑除法的意义。
	课件上的例子：(Interval attributes) calendar dates, **temperatures in Celsius or Fahrenheit**, GRE score; (Ratio attributes) **temperature in Kelvin**, length, time, counts

备注，GRE 分数我个人理解应该是 Ratio 的，而 Customer ID 比如 202002223 这种是有序的，但是 1asfaf4213 这种就是无序的。

**老师的结论是不考这种有争议的。**

----

运算支持 Distinctness $=,\ne$	 Order $<,>$	 Addition $+,-$	 Multiplication $\times,/$

Nominal attribute: distinctness	Ordinal attribute: distinctness & order	Interval attribute: distinctness, order & addition	Ratio attribute: all 4 properties

## 数据表征

Record Data: 由一组记录组成的数据，每个记录由固定的属性 / 功能功能组成，可以组成 Data Matrix。

Document Data BOW 方法：首先得到所有文档中的全部单词，而后统计每篇文档中出现某个单词的次数。**直观上就是每个词在每篇文章中出现的次数。**

**TF-IDF**：TF （词频）为某个词在某篇文章中出现的比例，也即单词 w 在文章中出现的次数 / 文章总共的单词数。IDF （逆文本频率）为 log(总共文章数目 / 包含 w 的文章数目)。一片文章的特征就是每个词的 tf \* idf 组成的向量。

 Transaction Data：交易数据，一类特殊的 Record Data

## 数据描述

