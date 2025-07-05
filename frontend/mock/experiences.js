export const experiences = [
  {
    id: 1,
    company: "字节跳动",
    position: "前端工程师",
    summary: "面试分三轮，主要考察React、算法和项目经验。",
    content: "第一轮：自我介绍+React原理+手写Promise。第二轮：算法题+项目优化。第三轮：主管面，聊职业规划。",
    tags: ["React", "算法", "大厂"],
    difficulty: 4,
    user: { id: 1, username: "小明", avatar: "" },
    created_at: "2024-06-01",
  },
  {
    id: 2,
    company: "腾讯",
    position: "后端开发",
    summary: "主要问了数据库、分布式和项目架构。",
    content: "一面：MySQL索引、Redis缓存。二面：分布式锁、消息队列。三面：系统设计。",
    tags: ["MySQL", "分布式", "Redis"],
    difficulty: 5,
    user: { id: 2, username: "小红", avatar: "" },
    created_at: "2024-05-28",
  },
  // ...更多数据
];
