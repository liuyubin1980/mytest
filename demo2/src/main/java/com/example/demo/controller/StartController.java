package com.example.demo.controller;
import com.example.entity.User;
import com.example.mapper.UserMapper;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;
import java.sql.*;
import java.util.*;

@RestController
//@RequestMapping("/start")
public class StartController {
//    @GetMapping("/index")
//    public String index(Model model){
//        model.addAttribute("title","第一个页面");
//        model.addAttribute("join","页面的测试内容");
//        return "index";
//
//    }
//test liuyubin 2025-8-11 20:32:04
    @RequestMapping("/test404")
    public String test404() {
        return "index";
    }
    @RequestMapping("/test500")
    public String test500() {
        int i = 1 / 0;
        return "index";
    }



    @RequestMapping("/springboot")
    public User startSpringBoot() {
        return new User("测试", 30);

//        return "Welcome to the world of Spring Boot!";
    }
    @PostMapping ("/jason")
    public List<User> retureJason(@RequestParam String username,@RequestParam String age) {
        System.out.println("获取到的username为：" + username);
        Integer a = Integer.parseInt(age);


        List<User> userList = new ArrayList<>();
        User user1 = new User(username, a);
        User user2 = new User("测试课", 42);
//        user1.setAge(3);
        userList.add(user1);
        userList.add(user2);
        return userList;
    }
    @PostMapping ("/qury")
    public String quryuser(){
        //声明Connection对象
        Connection con;
        //驱动程序名
        String driver = "org.postgresql.Driver";
        //URL指向要访问的数据库名liuyubindb
        String url = "jdbc:postgresql://192.168.56.103:26000/liuyubindb";
        //用户名
        String user = "gem";
        //密码
        String password = "OpenGauss@123";
        //遍历查询结果集
        try {
            //加载驱动程序
            Class.forName(driver);
            //1.getConnection()方法，连接数据库！！
            con = DriverManager.getConnection(url,user,password);
            if(!con.isClosed())
                System.out.println("Succeeded connecting to the Database!");
            //2.创建statement类对象，用来执行SQL语句！！
            Statement statement = con.createStatement();
            //要执行的SQL语句
            String sql = "select * from my_db.t_demo1";
            //3.ResultSet类，用来存放获取的结果集！！
            ResultSet rs = statement.executeQuery(sql);
            System.out.println("-----------------");
            System.out.println("执行结果如下所示:");
            System.out.println("-----------------");
            System.out.println("ID" + "\t" + "姓名");
            System.out.println("-----------------");
            String job = null;
            String id = null;
            while(rs.next()){
                //获取stuname这列数据
                job = rs.getString("name");
                //获取stuid这列数据
                id = rs.getString("id");
                //输出结果
                System.out.println(id + "\t" + job);
            }
            rs.close();
            con.close();
        } catch(ClassNotFoundException e) {
            //数据库驱动类异常处理
            System.out.println("Sorry,can`t find the Driver!");
            e.printStackTrace();
        } catch(SQLException e) {
            //数据库连接失败异常处理
            e.printStackTrace();
        }catch (Exception e) {
            // TODO: handle exception
            e.printStackTrace();
        }finally{
            System.out.println("数据库数据成功获取！！");
        }
        return "";
    }
    @Autowired
    private UserMapper userMapper;
    @PostMapping ("/qury2")
    public List<User> quryuser2(){
//        @Autowired
//        UserMapper userMapper;
//        return userMapper.getall();

        User a = new User("a",12);
        User b = new User("b",13);
        List<User> List_a = List.of(a, b);
        return List_a;

    }


    @PostMapping ("/adduser")
    public void addUser(){
        userMapper.addUser();

    }


}