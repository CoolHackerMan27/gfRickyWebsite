<script>
    import { goto } from "$app/navigation"
    import home from '$lib/assets/house.png';
    import star1 from '$lib/assets/star1.png';


    function uploadFiles(){
        //opens file dialog and uploads files to server
        const input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        input.onchange = async () => {
            if (!(input.files)){ 
                return;
            }
            const files = Array.from(input.files);
            const formData = new FormData();
            files.forEach(file => formData.append('files', file));
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    alert('Files uploaded successfully!');
                } else {
                    alert('Upload failed.');
                }
            } catch (error) {
                console.error('Error uploading files:', error);
                alert('An error occurred during upload.');
            }
        };
        input.click();
    }

</script>
<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        height: 100vh;
        background-color: #f6ebc6;
        position: relative;
        overflow: hidden;
    }

    /* Floating stars */
    .stars {
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }
    .star {
        position: absolute;
        font-size: 1.5rem;
        opacity: 0.6;
        animation: float 6s ease-in-out infinite;
    }
    .star:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
    .star:nth-child(2) { left: 25%; top: 60%; animation-delay: 1s; font-size: 1rem; }
    .star:nth-child(3) { left: 50%; top: 30%; animation-delay: 2s; }
    .star:nth-child(4) { left: 70%; top: 70%; animation-delay: 3s; font-size: 2rem; }
    .star:nth-child(5) { left: 85%; top: 15%; animation-delay: 4s; }
    .star:nth-child(6) { left: 15%; top: 80%; animation-delay: 2.5s; font-size: 1.2rem; }
    .star:nth-child(7) { left: 60%; top: 85%; animation-delay: 1.5s; }
    .star:nth-child(8) { left: 90%; top: 45%; animation-delay: 3.5s; font-size: 1rem; }

    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-50px) rotate(10deg); }
        25% { transform: translateY(-25px) rotate(90deg); }
        75% { transform: translateY(-20px) rotate(-25deg); }
        37.5% { transform: translateY(-40px) rotate(-45deg); }
    }

    /* Keep content above stars */
    .banner, .details, .songs, p {
        position: relative;
        z-index: 1;
    }

    .banner {
        width: 100%;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: flex-start;
        padding: 20px;
        gap: 20px;
    }
    .homeBtn {
        background-color: #5276b4;
        color: #f6ebc6;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 16px 32px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 4px 4px 0px #333;
    }
    .homeBtn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #333;
    }
    .introCard {
        background-color: #5276b4;
        color: #f6ebc6;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 16px 32px;
        font-size: 1.5rem;
        font-weight: bold;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 4px 4px 0px #333;
    }
    .uploadBtn {
        background-color: #5276b4;
        color: #f6ebc6;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 16px 32px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 4px 4px 0px #333;
    }
    .uploadBtn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #333;
    }

    .details {
        margin-top: 40px;
        width: 100%;
        height: 20%;
        color: #f6ebc6;
        border-radius: 8px;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: flex-start;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 16px 32px;
    }
    .minutesCard, .songsCard, .albumsCard {
        background-color: #5276b4;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 32px 32px;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 4px 4px 0px #333;
        margin-right: 20px;
        margin-left: 20px;
    }
    .songs {
        margin-top: 40px;
        width: 100%;
        height: 80%;
        color: #f6ebc6;
        border-radius: 8px;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: flex-start;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 16px 32px;
    }
    .songsListend, .percentListened {
        background-color: #5276b4;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 32px 32px;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 4px 4px 0px #333;
        margin-right: 20px;
        margin-left: 20px;
    }

</style>


<div class="container">
    <!-- Floating stars background -->
    <div class="stars">
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
        <img src={star1} alt="Star" class="star" style="height:25px; width:25px;" />
               
    </div>

    <div class= "banner">
        <button class="homeBtn" on:click={() => goto("/")}>
            <img src={home} alt="Home" style="width: 24px; height: 24px;" />
        </button>
        <card class="introCard"> your stats   </card>
        <button class="uploadBtn" on:click={uploadFiles}>
            Upload Files
        </button>
    </div>
    <div class= "details">
        <card class="minutesCard"> you listened to __ minutes</card>
        <card class="songsCard">you listened to __ songs</card>
        <card class="albumsCard"> you listened to __ albums</card>
    </div>
    <div class= "songs">
        <card class="songsListend">This will be a list of songs</card>
        <card class="percentListened">Show what % has been listed to of his songs</card>
    </div>
    
</div>