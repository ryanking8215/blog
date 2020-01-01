---
title: "测试替身-Fake,Stub,Mock"
date: 2019-12-31T11:42:52+08:00
categories: ["Tech"]
tags: ["testing", "测试"]
keywords:
  - testing
  - 测试
  - mock
description: 描述了3种测试替身类型, 并且使用go实现example
draft: true
---

最近在网上看到[这篇博文](https://dev.to/milipski/test-doubles---fakes-mocks-and-stubs), 博文介绍了几种"测试替身(test doubles)"的方式和Java例子。

这里进行简单的翻译，并给出golang的example.

>In automated testing it is common to use objects that look and behave like their production equivalents, but are actually simplified. This reduces complexity, allows to verify code independently from the rest of the system and sometimes it is even necessary to execute self validating tests at all. A Test Double is a generic term used for these objects.


在自动化测试领域，普遍使用和生产代码类似，但更简化的对象来测试。这减小了复杂度，并且能和系统其它部分做很好的隔离，可以单独验证。这种对象有个术语，叫"测试替身"。


>Although test doubles come in many flavors (Gerard Meszaros introduced five types in this article), people tend to use term Mock to refer to different kinds of test doubles. Misunderstanding and mixing test doubles implementation may influence test design and increase fragility of tests, standing on our way to seamless refactorings.

"测试替身"有好几种方式([这篇文章](http://xunitpatterns.com/Test%20Double.html)介绍了有5种), 人们一般都是用术语"Mock"来指代这些不同类型的"测试替身"。误解和混淆这些测试替身会影响测试设计，增加测试脆弱性，阻碍我们的持续重构。

>In this article I will describe three implementation variations of testing doubles: Fake, Stub and Mock and give you examples when to use them.

原作者介绍3种"测试替身"的实现，Fake, Stub和Mock, 并且给出例子说明什么时候去使用。

## Fake
> Fakes are objects that have working implementations, but not same as production one. Usually they take some shortcut and have simplified version of production code.

Fake对象有可工作的实现，但是和生产环境的不同。通常他们是生产环境代码的简化版本.

![](/images/test_doubles/fake.png)

```golang
type AccountRepository interface {
    GetPasswordHash(user *User) string
}

// FakeAccountRepository implements AccountRepository
var _ AccountRepository = (* FakeAccountRepository)(nil)

type FakeAccountRepository struct {
    accounts map[string]*Account // key is user's unique email
}

func NewFakeAccountRepository() *FakeAccountRepository {
    return &FakeAccountRepository{
        accounts: map[string]*Account{
        "john@bmail.com": NewAccount(),
        "boby@bmail.com": NewAccount(),
        }
    }
}

func (r *FakeAccountRepository) GetPasswordHash(user *User) string {
    a := r.accounts[user.Email]
    return a.PasswordHash()
}
```

本人觉得这个例子作者举的不好，Fake对象应该重点突出"可工作实现"，如果还是以Repository来举例，可以是:
```golang
type AccountRepository interface {
    Find() ([]*Accounts, error)
    Add(user *User) (*Account, error)
    Get(user *User) (*Account, error)
    Delete(user *User) error
}
```

FakeAccountRepositry可以是in-memory的实现，来代替真正的"Database"实现。

但是FakeAccountRepository本身是可工作的,对每个接口都能正确响应。


## Stub
>Stub is an object that holds predefined data and uses it to answer calls during tests. It is used when we cannot or don’t want to involve objects that would answer with real data or have undesirable side effects.

Stub对象在测试过程中使用预定义的数据响应外部调用。当我们不能或不想引入真实数据的响应，或者不想有副作用时使用。

![](/images/test_doubles/stub.png)

原作者Java的例子里，"GradeService"是待测试对象，它调用了"Gradebook"对象来实现"averageGrades"方法,
我对Java不是很熟悉，从代码看，使用了Java测试框架，通过反射得到一个"Gradebook"的Mock对象。在测试用例里，通过Mock对象来生成数据，继而对方法正确性进行测试。

在golang里对具体类型进行Mock，好像不太容易办到，所以在构建代码时让interface介入，待测试对象还是"GradeService", 但是"Gradebook"是一个interface，而非具体类型。

```golang
type IGradebook interface {
    GradesFor(s *Student) map[string]float32 // map[string]int, key is subject, value is score
}

var _ IGradebook = (* RealGradebook)(nil)

type RealGradebook struct {
}

func (gb *RealGradebook) GradesFor(s *Student) map[string]float32 {
  // real implements
}

type GradeService struct {
    gradebook IGradebook
}

func NewGradeService(gb IGradebook) *GradeService {
    return &GradeService {
        gradebook: gb,
    }
}

func (s *GradeService) AverageGrades(student *Student) float32 {
    grades := s.gb.GradeFor(student)
    sum:= float32(0.0)
    for _, score:=range grades {
        sum+=score
    }
    if len(grades) == 0 {
        return 0
    } 
    return sum/float32(len(grades))
}
```

既然"GradeService" hold的是接口类型，那么我们可以实现一个StubGradebook类型，返回预定义好的数据。
```golang

var _ IGradebook = (* StubGradebook)(nil)

type StunGradebook struct {
}

func (gb *StubGradebook) GradesFor(s *Student) map[string]float32 {
  return map[string]float32{
    "OOP": 8,
    "FP": 6,
    "DB": 10,
  }
}

func Test_GradeService_AverageGrades(t *testing.T) {
  svc:=NewGradeService(&StubGradebook{})
  v:=svc.AverageGrades(&Student{})
  if v != 8.0 {
    t.Errorf("average grades wrong")
  }
}
```

另外也可以使用[testify库](https://github.com/stretchr/testify)的mock包来做测试：
```golang
// TODO
```

## Command Query Separation
>Methods that return some result and do not change the state of the system, are called Query. Method avarangeGrades, that returns average of student grades is a good example: Double getAverageGrades(Student student);  
>
>It returns a value and is free of side effects. As we have seen in students grading example, for testing this type of method we use Stubs. We are replacing real functionality to provide values needed for method to perform its job. Then, values returned by the method can be used for assertions.
>
>There is also another category of methods called Command. This is when a method performs some actions, that changes the system state, but we don’t expect any return value from it: void sendReminderEmail(Student student);
>
>A good practice is to divide an object's methods into those two separated categories.
>This practice was named: Command Query separation by Bertrand Meyer in his book "Object Oriented Software Construction".
>
>For testing Query type methods we should prefer use of Stubs as we can verify method’s return value. But what about Command type of methods, like method sending an e-mail? How to test them when they do not return any values? The answer is Mock - the last type of test dummy we gonna cover.

这一段比较冗长，大意是类似于"GradeService"的测试用例，是一种"查询"，它不改变系统状态, 仅返回数据；还有一种叫"命令", 执行"命令"会改变系统状态，或者让系统发生了副作用，例如发送邮件。所以要将这两者区分开发，那么我们怎么来测试呢后者呢？我们总不能每次测试真的去发送邮件，针对这种情况,引入了Mock。

## Mock
>Mocks are objects that register calls they receive. In test assertion we can verify on Mocks that all expected actions were performed.

Mock对象记录他们接收到的调用，在测试过程中我们通过检查Mock对象来确认所有的预期动作被执行了。

![](/images/test_doubles/mock.png)

# 后记
## 总结
如果你看得一头雾水的话，可以看下我的总结：
* Fake - 着重"可工作"实现，可以用简单便捷的方式来实现, 逻辑功能不能缺，不能像stub那样编造数据，也不能像mock假执行。
* Stub - 返回预定义的数据。
* Mock - 验证方法被执行了。
  
实际上stub返回数据，那对应方法肯定被执行了，mock也会执行方法，看上去mock像是不返回数据的stub的特例。

原作者从"查询"和"命令"的角度去区分两者，"查询"返回数据，"命令"不返回数据。

我到觉得有更本质的区别：
**mock对象是待测试对象; 而stub对象不是，stub对象是为待测试对象做嫁衣。**

## 不要混淆测试替身和库的命名
无论是Java还是golang的例子，都可以看到，"stub"类型的测试替身可以由mock库(包)来实现。
前者是"测试替身"类型，是从用处和用法出发的概念；后者是库，是具体的实现；在说明时不要混淆了。

## 吐槽
Java下可以简单的使用mock对象，但是golang需要先建立interface, 测试替身才可以介入，但是很多时候，开发时的抽象是面向业务的，是适度和可控的，如果仅为了测试而增加interface，有过度设计的嫌疑，整个项目几乎不能看了。

所以，在描述Stub那段，照搬Java的例子使用golang去实现，有点照猫画虎，如果为了验证AverageGrades方法是否正确

我会定义方法:
```golang
func (s *GradeService) averageGrades(scores []float32) float32 {
  // implements
}
```
这样可以编造任意的socres slice来测试，而不用费劲去stubing gradebook.

# 参考
* https://dev.to/milipski/test-doubles---fakes-mocks-and-stubs
* https://zhuanlan.zhihu.com/p/26942686
* https://github.com/utkarsh17ife/goMockPractice
