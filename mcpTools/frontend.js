// document.getElementById("genBlog").addEventListener("click", function() {
//     console.log("button click");
//     let numbers = document.getElementById("numbers").value.split(",");  // input -> array
//     let num = numbers[0]; // userPhoneNum
//     let customerNumbers = numbers.slice(1); // rest -> custPhoneNums

//     customerNumbers.forEach(element => {
//       axios.post("http://127.0.0.1:8000/calltool", {
//         custPhoneNum: element.trim(),
//         userPhoneNum: num.trim()
//       })
//       .then(res => {
//         console.log("✅ Success:", res.data);
//       })
//       .catch(err => {
//         console.error("❌ Error:", err);
//       });
//     });
//   });

document.addEventListener("DOMContentLoaded", () => {
    // const genBlogBtn = document.getElementById("genBlog") || document.getElementById("sendChat");
    const genBlogBtn = document.getElementById("sendChat");
    console.log(genBlogBtn);
    
//     function appendChat(from, msg) {
//     const el = document.createElement('div');
//     el.innerHTML = `<strong>${from}:</strong> ${msg}`;
//     const area = document.getElementById('chatArea');
//     if (!area) return console.error("❌ chatArea not found");
//     area.appendChild(el);
//     area.scrollTop = area.scrollHeight;
//   }

    if (!genBlogBtn) {
        console.warn("genBlog button not found");
        return;
    }

    genBlogBtn.addEventListener("click", () => {
        console.log("button click");
        // const promptData = document.getElementById("blogAi").value || document.getElementById("chatInput").value;
        const promptData = document.getElementById("chatInput").value;
        if (!promptData) return alert("Please enter a prompt!");

        console.log("first number:", promptData);
        axios.post("http://127.0.0.1:8000/ask-gemini", {
            "prompt": promptData
        })
            .then(res => {
                console.log(res)
                if (res?.data?.tool=="prompt_blogs"){
                console.log("✅ Success:", res.data.result);

                const container = document.querySelector(".blockedAnswers");

                // ek naya div banao har answer ke liye
                const newAns = document.createElement("div");
                newAns.classList.add("answer-box");
                if (res?.data?.result?.result)
                newAns.innerHTML = res.data.result.result || res.data.result;
                else{
                    newAns.innerHTML=res.text
                }

                // append to container
                container.appendChild(newAns);

                // show panel
                document.getElementById("blog-panel").style.display = "block";
            }
            else {
                    console.log("element is this one", res?.data?.response);

                    const chatArea = document.getElementById("chatArea");
                    if (chatArea) {
                        const el = document.createElement("div");
                        el.className = "system";
                        el.innerHTML = `<strong>AI:</strong> ${res?.data?.response || '(no response)'}`;
                        chatArea.appendChild(el);
                        chatArea.scrollTop = chatArea.scrollHeight;
                    } else {
                        console.error("❌ chatArea not found in DOM");
                    }
                }
            })

      .catch (err => {
            console.error("❌ Error:", err);
        });

});
});
