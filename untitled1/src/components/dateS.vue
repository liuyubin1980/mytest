<template>
  <div class="timebox">
    <div class="shortcut" v-if="timeCount.length">
      <p
          v-for="(item, index) in timeCount"
          :key="index"
          @click="jumpShortcut(item.timeDiff)"
      >
        {{ item.title }}
      </p>
    </div>
    <!-- 日历部分-->
    <div id="calendar">
      <!-- 年份  -->
      <div class="month">
        <!-- 时间切换 -->
        <div class="time-switch">
          <!-- 上一年 -->
          <div
              class="arrow hands iconfont icon-xiangzuo"
              @click="pickPre(currentYear, currentMonth, 'Y')"
          ></div>
          <!-- 上个月 -->
          <div
              class="arrow hands iconfont icon-xiangzuodan"
              @click="pickPre(currentYear, currentMonth)"
          ></div>
          <div class="year-month">
            <span class="choose-year">{{ currentYear }} 年 </span>
            <span class="choose-month">{{ currentMonth }} 月 </span>
          </div>
          <!-- 下个月 -->
          <div
              class="arrow hands iconfont icon-xiangyoudan"
              @click="pickNext(currentYear, currentMonth)"
          ></div>
          <!-- 下一年 -->
          <div
              class="arrow hands iconfont icon-xiangyou"
              @click="pickNext(currentYear, currentMonth, 'Y')"
          ></div>
        </div>
      </div>
      <!-- 星期 -->
      <ul class="weekdays">
        <li>日</li>
        <li>一</li>
        <li>二</li>
        <li>三</li>
        <li>四</li>
        <li>五</li>
        <li>六</li>
      </ul>
      <!-- 日期 -->
      <div class="days">
        <!-- 核心 v-for循环 每一次循环用<li>标签创建一天 -->
        <div v-for="dayobject in days" :key="dayobject" class="days-item">
          <!--不是本月day-->
          <div
              v-if="dayobject.day.getMonth() + 1 != currentMonth"
              class="other-day"
              :class="{
              prohibit:
                (minTime && dayobject.day.getTime() < minTime) ||
                (maxTime && dayobject.day.getTime() > maxTime)
            }"
              @click="getDayTime(dayobject.day)"
          >
            <p>{{ dayobject.day.getDate() }}</p>
          </div>
          <!--本月day-->
          <div class="current-month" v-else>
            <div
                class="item-day"
                @click="getDayTime(dayobject.day)"
                :class="[
                newDate == formatDateYMD(dayobject.day) ? 'active' : '',
                {
                  prohibit:
                    (minTime && dayobject.day.getTime() < minTime) ||
                    (maxTime && dayobject.day.getTime() > maxTime)
                }
              ]"
            >
              <p>{{ dayobject.day.getDate() }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs, onBeforeMount, onMounted } from 'vue';
export default {
  name: 'dataS',
  props: {
    isCompletionZero: {
      type: Boolean,
      default: true,
      explain: '是否补齐日期中各位字符前的0',
      otherVal: 'false'
    },
    dateFormat: {
      type: String,
      default: 'Ch',
      explain: '日期拼接格式（Ch是年月日格式，或者设置拼接符号）',
      otherVal: '- ：/'
    },
    minTime: {
      type: Number,
      default: 0,
      explain: '限制可切换的最小时间',
      otherVal: '时间戳'
    },
    maxTime: {
      type: Number,
      default: 0,
      explain: '限制可切换的最大时间',
      otherVal: '时间戳'
    },
    shortcutMenu:{
      type: Array,
      default: ()=>{
        return []
      },
      explain: '快捷菜单配置（title：快捷键名称,timeDiff：时间偏移量）',
      otherVal: `[
        { title: '今天', timeDiff: 0 }
        { title: '昨天', timeDiff: 偏移的时间戳 }]`
    },
    dateChange:{
      type: Function,
      explain: `获取选择的日期（format:当前选择的格式化日期,stamp:当前选择时间戳,type:'选择类型点击或者快捷'）`
    }

  },
  setup(props,ctx) {
    const data = reactive({
      timeCount: [], //时间快捷
      currentDay: 1,
      currentMonth: 1,
      currentYear: 2023, //当前年
      currentWeek: 1,
      days: [],
      newDate: '' //当前日期
    });
    onBeforeMount(() => {});
    onMounted(() => {
      data.timeCount = props.shortcutMenu
      data.newDate = formatDateYMD(new Date());
    });
    // 初始日期
    const initData = (cur) => {
      // let leftcount = 0 // 存放剩余数量
      let date;
      if (cur) {
        date = new Date(cur);
      } else {
        const now = new Date();
        const d = new Date(formatDate(now.getFullYear(), now.getMonth(), 1));
        d.setDate(35);
        date = new Date(formatDate(d.getFullYear(), d.getMonth() + 1, 1));
      }
      data.currentDay = date.getDate();
      data.currentYear = date.getFullYear();
      data.currentMonth = date.getMonth() + 1;
      data.currentWeek = date.getDay(); // 1...6,0
      if (data.currentWeek === 0) {
        data.currentWeek = 7;
      }
      let str = formatDate(
          data.currentYear,
          data.currentMonth,
          data.currentDay
      );
      data.days.length = 0;
      // 今天是周日，放在第一行第7个位置，前面6个
      // 初始化本周
      for (let i = data.currentWeek; i >= 0; i--) {
        let d2 = new Date(str);
        d2.setDate(d2.getDate() - i);
        let dayobjectSelf = {}; // 用一个对象包装Date对象  以便为以后预定功能添加属性
        dayobjectSelf.day = d2;
        data.days.push(dayobjectSelf); // 将日期放入data 中的days数组 供页面渲染使用
      }
      // 其他周
      for (let j = 1; j < 42 - data.currentWeek; j++) {
        let d3 = new Date(str);
        d3.setDate(d3.getDate() + j);
        let dayobjectOther = {};
        dayobjectOther.day = d3;
        data.days.push(dayobjectOther);
      }
      // 下面方法对多余天数进行截取处理
      // dayListHandle();
    };
    // 对天数数据进行多余截取
    const dayListHandle = () => {
      // 判断当前日历中是不是包含今天，控制是否显示跳转今日的按键
      const currentY = new Date().getFullYear();
      const currentM = new Date().getMonth() + 1;
      data.showTodayBtn =
          data.currentYear !== currentY || data.currentMonth !== currentM;
      // 下面处理多余其他月的天数
      let frontNum = 0; //前
      let afterNum = 0; //后
      data.days.forEach((item, index) => {
        // 每一项的月份
        const inCurrentMonth = item.day.getMonth() + 1;
        const halfLength = data.days.length / 2;
        if (data.currentMonth === inCurrentMonth) return; // 和当前月份相等就不在执行
        if (index < halfLength) {
          frontNum++;
        } else {
          afterNum++;
        }
      });
      if (afterNum < 7 && frontNum < 7) return;
      if (afterNum > 6) {
        // console.log('后截取');
        data.days = data.days.splice(0, data.days.length - 7);
      }
      if (frontNum > 6) {
        // console.log('前截取');
        data.days = data.days.splice(7);
      }
      // 最终展示的天数 42、35、28三个数量
      // console.log(data.days);
    };
    // 快捷跳转
    // timeDiff  正负 前后移动的时间戳ms
    const jumpShortcut = (timeDiff) => {
      let thenTime = new Date();
      // 计算需要跳转的时间戳
      thenTime.setTime(thenTime.getTime() + timeDiff);
      if (
          (props.minTime && thenTime.getTime() < props.minTime) ||
          (props.maxTime && thenTime.getTime() > props.maxTime)
      )
        return;
      // 根据跳转的时间切换日历
      const currentY = thenTime.getFullYear();
      const currentM = thenTime.getMonth() + 1;
      pickNext(currentY, currentM - 1);

      data.newDate = formatDateYMD(thenTime); //例如：2023年2月23日
      console.log('快捷', data.newDate);
      console.log('快捷时间戳', thenTime.getTime());
      ctx.emit('dateChange',{format:data.newDate,stamp:thenTime.getTime(),type:'shortcut'})
    };
    // 点击日期
    const getDayTime = (el) => {
      let timeMs = el.getTime();
      // 判断时间选择控制范围
      if (
          (props.minTime && timeMs < props.minTime) ||
          (props.maxTime && timeMs > props.maxTime)
      )
        return;
      data.newDate = formatDateYMD(el);
      // 点击其他月份直接跳转，到指定月份
      if (data.currentMonth < el.getMonth() + 1) {
        pickNext(data.currentYear, data.currentMonth);
      }
      if (data.currentMonth > el.getMonth() + 1) {
        pickPre(data.currentYear, data.currentMonth);
      }
      console.log('手动点击', data.newDate);
      console.log('手动点击时间戳', timeMs);
      ctx.emit('dateChange',{format:data.newDate,stamp:timeMs,type:'click'})
    };
    // 上个月
    const pickPre = (year, month, type) => {
      let m = month;
      let y = year;
      if (type === 'Y') {
        y -= 1;
      } else {
        if (m === 1) {
          y -= 1;
          m = 12;
        } else {
          m -= 1;
        }
      }
      initData(formatDate(y, m, 1));
    };
    // 下个月
    const pickNext = (year, month, type) => {
      let m = month;
      let y = year;
      if (type === 'Y') {
        y += 1;
      } else {
        if (m === 12) {
          y += 1;
          m = 1;
        } else {
          m += 1;
        }
      }
      initData(formatDate(y, m, 1));
    };
    // 返回 类似 2022-05-17 格式的字符串
    const formatDate = (year, month, day) => {
      let y = year;
      let m = month;
      if (m < 10) m = '0' + m;
      let d = day;
      if (d < 10) d = '0' + d;
      return y + '-' + m + '-' + d;
    };
    // 日期格式化，个位数不增加0，2023年2月7日
    const formatDateYMD = (date) => {
      let y = date.getFullYear();
      let m = date.getMonth() + 1;
      let d = date.getDate();
      // 是否补齐0
      if (props.isCompletionZero) {
        m = m < 10 ? '0' + m : m;
        d = d < 10 ? '0' + d : d;
      }
      // 年月日拼接符号
      // 默认年月日
      let returnDate = `${y}年${m}月${d}日`;
      if (props.dateFormat !== 'Ch') {
        // 符号拼接
        const symbol = props.dateFormat;
        returnDate = `${y}${symbol}${m}${symbol}${d}`;
      }
      return returnDate;
    };
    // 判断是不是今天
    const isToday = (day) => {
      return (
          day.getFullYear() == new Date().getFullYear() &&
          day.getMonth() == new Date().getMonth() &&
          day.getDate() == new Date().getDate()
      );
    };
    initData(null);
    return {
      jumpShortcut,
      pickPre,
      pickNext,
      getDayTime,
      isToday,
      formatDateYMD,
      ...toRefs(data)
    };
  }
};
</script>
<style scoped lang="less">
.timebox {

  // width: 600px;
  background: #fff;
  overflow: hidden;
  display: flex;
  .shortcut {
    width: 100px;
    font-size: 14px;
    line-height: 26px;
    padding: 10px;
    box-sizing: border-box;
    color: #606266;
    border-right: 1px solid #ddd;
    cursor: pointer;
    transition: 0.3s;
    p {
      &:hover {
        transform: scale(1.05);
        color: #606266;
      }
    }
  }
  #calendar {
    width: 320px;
    padding: 10px 20px;
    cursor: pointer;
    background: #fff;
    border-radius: 5px;
    .month {
      width: 100%;
      font-size: 16px;
      overflow: hidden;
      .time-switch {
        display: flex;
        height: 26px;
        line-height: 26px;
        .year-month {
          flex: 4;
          text-align: center;
          width: 200px;
          color: #606266;
        }
        .arrow {
          flex: 1;
          font-size: 14px;
          text-align: center;
          opacity: 0.5;
          &:hover {
            opacity: 1;
          }
        }
      }
    }
    .weekdays {
      overflow: hidden;
      padding: 10px 0;
      line-height: 20px;
      border-bottom: 1px solid #606266;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      li {
        width: 14%;
        float: left;
        text-align: center;
        color: #606266;
        font-size: 12px;
      }
    }
    .days {
      overflow: hidden;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      .days-item {
        width: 14%;
        height: 40px;
        float: left;
        text-align: center;
        color: #606266;
        box-sizing: border-box;
        font-size: 12px;
        transition: 0.3s;
        line-height: 40px;
        position: relative;
        &:hover {
          color: #dddddd;
        }
        .item-day,
        .other-day {
          height: 100%;
          box-sizing: border-box;
          transition: 0.3s;
          height: 30px;
          line-height: 30px;
          margin-top: 5px;
          &.active {
            p {
              margin: 0 auto;
              width: 30px;
              border-radius: 20px;
              background: #606266;
              color: #fff;
            }
          }
          &.prohibit {
            background: #42b983;
            color: #dddddd;
          }
        }
        .current-month {
          height: 100%;
        }
        .other-day {
          color: #606266;
        }
      }
    }
  }
}
</style>