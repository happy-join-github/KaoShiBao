// // const axiosInstance = window.$nuxt.$axios;
// // // 插入响应拦截器（放在最后面，确保在解密之后执行）
// // axiosInstance.interceptors.response.use(function (response) {
// //     // 只捕获题目批量接口
// //     if (response.config && response.config.url && response.config.url.includes('/questions/ids')) {
// //         // console.clear();  // 可选：清屏让日志更醒目
// //         // console.log('%c=== 成功捕获解密后的明文数据 ===', 'color:white;background:#67c23a;font-size:16px;padding:10px;border-radius:5px;font-weight:bold;');
// //         // console.log('请求参数（ids）:', JSON.parse(response.config.data).ids);
// //         // console.log('完整返回数据:', response.data);

// //         // 保存到全局变量，方便你随时查看或复制
// //         window.lastDecryptedQuestions = response.data;
// //         // window.lastQuestionIds = JSON.parse(response.config.data).ids;

// //         // 漂亮表格展示每道题关键信息
// //         // if (response.data.data && Array.isArray(response.data.data)) {
// //         //     console.table(response.data.data.map(q => ({
// //         //         id: q.id,
// //         //         qtype: q.qtype + (q.qtype == 1 ? '（单选）' : q.qtype == 2 ? '（多选）' : q.qtype == 4 ? '（填空）' : ''),
// //         //         question: q.question.replace(/<[^>]+>/g, '').substring(0, 80) + '...',  // 去标签截断
// //         //         answer: q.answer,
// //         //         answerC: q.answerC || '无'
// //         //     })));
// //         // }
// //         // console.log('%c数据已保存：输入 window.lastDecryptedQuestions 查看完整数据', 'color:#409eff;font-size:14px;');
// //     }

// //     return response;
// // }, function (error) {
// //     return Promise.reject(error);
// // });


// // 注入时机，在页面还每点击顺序刷题的时候，注入。 注入实例成功实例请看：hookimage.png

// const axiosInstance = window.$nuxt.$axios;
// window.DecryptedQuestions=[];
// // 插入响应拦截器（放在最后面，确保在解密之后执行）
// axiosInstance.interceptors.response.use(function (response) {
//     // 只捕获题目批量接口
//     if (response.config && response.config.url && response.config.url.includes('/questions/ids')) {
//         console.log('%c=== 成功捕获解密后的明文数据 ===', 'color:white;background:#67c23a;font-size:16px;padding:10px;border-radius:5px;font-weight:bold;');        
//         if (Array.isArray(response.data.data)){
//             window.DecryptedQuestions.push(response.data)
//         }
//         console.log('%c数据已保存：输入 window.DecryptedQuestions 查看完整数据', 'color:#409eff;font-size:14px;');
//     }

//     return response;
// }, function (error) {
//     return Promise.reject(error);
// });


const axiosInstance = window.$nuxt.$axios;window.DecryptedQuestions=[];axiosInstance.interceptors.response.use(function (response) {if (response.config && response.config.url && response.config.url.includes('/questions/ids')) {console.log('%c=== 成功捕获解密后的明文数据 ===', 'color:white;background:#67c23a;font-size:16px;padding:10px;border-radius:5px;font-weight:bold;');if (Array.isArray(response.data.data)){window.DecryptedQuestions.push(response.data)}}return response;}, function (error) {return Promise.reject(error);});console.log("注入完成");