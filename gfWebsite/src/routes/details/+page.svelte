<script>
    import { goto } from "$app/navigation"
    import { PUBLIC_PYTHON_API_URL } from "$env/static/public";
    import home from '$lib/assets/house.png';
    import star1 from '$lib/assets/star1.png';

    let isLoading = false;
    let songs = [];
    let albums = [];
    let percentSongs = 0;
    let percentAlbums = 0;
    let timeListened = 0;
    let rankedSongs = [];
    let numberOfSongs = 0;
    let numberOfAlbums = 0;
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
                isLoading = true;
                const response = await fetch(PUBLIC_PYTHON_API_URL + '/process-batch', {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    isLoading = false;
                    //Now we update the page with the new data
                    const data = await response.json();
                    console.log('Upload response:', data);
                    // Update UI with new data (e.g., refresh details view)
                    if (data.results && data.results.length > 0) {
                        const stats = data.results[0]; // Grab the first file processed

                        songs = stats.songs;
                        albums = stats.albums;
                        percentSongs = stats.percentSongs;
                        percentAlbums = stats.percentAlbums;
                        //# Fix formatting to look nice (e.g. 120 vs 120.43242)
                        timeListened = Math.round(stats.timeListened); 
                        rankedSongs = stats.ranked;
                        numberOfSongs = stats.numberOfSongs;
                        numberOfAlbums = stats.numberOfAlbums;
                    }
                    
                } else {
                    isLoading = false;
                    alert('Upload failed.');
                }
            } catch (error) {
                isLoading = false;
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
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        box-shadow: 4px 4px 0px #333;
        margin-right: 20px;
        margin-left: 20px;
        overflow-y: auto;
    }
    .songsListend h3, .percentListened h3 {
        margin: 0 0 16px 0;
        font-size: 1.4rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-bottom: 2px solid #f6ebc6;
        padding-bottom: 8px;
        width: 100%;
        text-align: center;
    }
    .songList {
        list-style: none;
        padding: 0;
        margin: 0;
        width: 100%;
        counter-reset: song;
    }
    .songList li {
        counter-increment: song;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 12px;
        margin-bottom: 6px;
        background-color: rgba(246, 235, 198, 0.12);
        border-radius: 6px;
        font-size: 1rem;
        font-weight: normal;
        transition: background-color 0.15s ease;
    }
    .songList li:hover {
        background-color: rgba(246, 235, 198, 0.22);
    }
    .songList li::before {
        content: counter(song);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 28px;
        height: 28px;
        background-color: #f6ebc6;
        color: #5276b4;
        border-radius: 50%;
        font-weight: bold;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    .songMs {
        margin-left: auto;
        font-size: 0.8rem;
        opacity: 0.7;
        white-space: nowrap;
    }
    .progressSection {
        width: 100%;
        margin-bottom: 20px;
    }
    .progressLabel {
        display: flex;
        justify-content: space-between;
        font-size: 0.95rem;
        margin-bottom: 6px;
        font-weight: normal;
    }
    .progressBar {
        width: 100%;
        background: rgba(51, 51, 51, 0.5);
        height: 14px;
        border-radius: 7px;
        overflow: hidden;
        border: 2px solid #333;
    }
    .progressFill {
        height: 100%;
        border-radius: 5px;
        background: #f6ebc6;
        transition: width 0.6s ease;
    }
    .waitingText {
        font-size: 1rem;
        font-weight: normal;
        opacity: 0.7;
        margin-top: 24px;
    }

    /* Loading overlay */
    .loadingOverlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(51, 51, 51, 0.7);
        z-index: 100;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;
    }
    .spinner {
        width: 60px;
        height: 60px;
        border: 5px solid rgba(246, 235, 198, 0.3);
        border-top: 5px solid #f6ebc6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    .loadingText {
        color: #f6ebc6;
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 1px;
    }

</style>


{#if isLoading}
    <div class="loadingOverlay">
        <div class="spinner"></div>
        <span class="loadingText">Crunching your data...(the backend server is slow af so it might take a while)</span>
    </div>
{/if}

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
        {#if timeListened > 0}
            <card class="minutesCard">You listened to {timeListened} minutes</card>
            <card class="songsCard">You listened to {numberOfSongs} unique songs</card>
            <card class="albumsCard">You listened to {numberOfAlbums} albums</card>
        {:else}
            <!-- Placeholder state before upload -->
            <card class="minutesCard">Upload data to see stats</card>
            <card class="songsCard">Upload data to see stats</card>
            <card class="albumsCard">Upload data to see stats</card>
        {/if}
    </div>

    <div class= "songs">
        <div class="songsListend">
            <h3>Top Songs</h3>
            {#if rankedSongs.length > 0}
                <ol class="songList">
                    {#each rankedSongs.slice(0, 5) as [songName, ms]}
                       <li>
                           <span>{songName}</span>
                           <span class="songMs">{Math.round(ms / 60000)} min</span>
                       </li>
                    {/each}
                </ol>
            {:else}
                <p class="waitingText">Waiting for data...</p>
            {/if}
        </div>
        
        <div class="percentListened">
            <h3>Completion</h3>
            {#if timeListened > 0}
                <div class="progressSection">
                    <div class="progressLabel">
                        <span>Songs</span>
                        <span>{percentSongs.toFixed(1)}%</span>
                    </div>
                    <div class="progressBar">
                        <div class="progressFill" style="width: {percentSongs}%;"></div>
                    </div>
                </div>
                <div class="progressSection">
                    <div class="progressLabel">
                        <span>Albums</span>
                        <span>{percentAlbums.toFixed(1)}%</span>
                    </div>
                    <div class="progressBar">
                        <div class="progressFill" style="width: {percentAlbums}%;"></div>
                    </div>
                </div>
            {:else}
                <p class="waitingText">Waiting for data...</p>
            {/if}
        </div>
    </div>
    <div>
    made with love by <a href="https://github.com/CoolHackerMan27/" target="_blank">Plank</a>
    </div>
    
</div>