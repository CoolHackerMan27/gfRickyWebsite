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
    /** @type {[string, number][]} */
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
                    
                    const data = await response.json();
                    console.log('Upload response:', data);
                    
                    if (data && data.songs) {
                        const stats = data; 

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
        min-height: 100vh;
        background-color: #f6ebc6;
        position: relative;
        overflow-x: hidden;
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
        max-width: 1200px;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: flex-start;
        padding: 20px;
        gap: 20px;
        box-sizing: border-box;
    }
    .bannerActions {
        display: contents;
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
        min-height: 44px;
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
        min-height: 44px;
    }
    .uploadBtn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #333;
    }

    .details {
        margin-top: 24px;
        width: 100%;
        max-width: 1200px;
        color: #f6ebc6;
        border-radius: 8px;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: flex-start;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 16px 32px;
        gap: 20px;
        box-sizing: border-box;
    }
    .minutesCard, .songsCard{
        background-color: #5276b4;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 32px 32px;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
       
        min-height: 120px;
        text-align: center;
    }
    .songs {
        margin-top: 24px;
        width: 100%;
        max-width: 1200px;
        color: #f6ebc6;
        border-radius: 8px;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: flex-start;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 16px 32px;
        gap: 20px;
        box-sizing: border-box;
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
       
        min-height: 280px;
        overflow: hidden;
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
        max-height: calc((44px + 6px) * 5);
        overflow-y: auto;
        scrollbar-gutter: stable;
        padding-right: 8px;
    }
    .songList li {
        counter-increment: song;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        margin-bottom: 6px;
        background-color: rgba(246, 235, 198, 0.12);
        border-radius: 6px;
        font-size: 1rem;
        font-weight: normal;
        transition: background-color 0.15s ease;
        min-height: 44px;
        box-sizing: border-box;
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
        text-align: center;
        padding: 0 16px;
    }

    @media (max-width: 900px) {
        .details, .songs {
            font-size: 1.2rem;
        }

        .introCard {
            font-size: 1.2rem;
        }
    }

    @media (max-width: 768px) {
        .stars {
            display: none;
        }

        .banner, .details, .songs {
            flex-direction: column;
            padding-left: 16px;
            padding-right: 16px;
            gap: 12px;
        }

        .bannerActions {
            display: flex;
            flex-direction: row;
            gap: 12px;
            width: 100%;
        }

        .bannerActions > * {
            width: 100%;
            box-sizing: border-box;
        }

        .banner {
            padding-top: 16px;
            padding-bottom: 0;
        }

        .introCard {
            width: 100%;
            flex: none;
            font-size: 1.1rem;
            box-sizing: border-box;
        }

        .details, .songs {
            margin-top: 16px;
            padding-top: 0;
            padding-bottom: 0;
            font-size: 1.1rem;
        }

        .homeBtn,
        .uploadBtn {
            width: 100%;
            box-sizing: border-box;
        }

        .minutesCard, .songsCard, 
        .songsListend, .percentListened {
            width: 100%;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }

        .songsListend, .percentListened {
            min-height: 200px;
        }

        .songList {
            max-height: calc((44px + 6px) * 5);
        }

        .songsListend h3, .percentListened h3 {
            font-size: 1.1rem;
        }
    }

    @media (max-width: 480px) {
        .homeBtn,
        .uploadBtn {
            padding: 12px 16px;
        }

        .minutesCard, .songsCard, 
        .songsListend, .percentListened {
            padding: 16px;
        }

        .songList li {
            gap: 8px;
            font-size: 0.95rem;
        }

        .songMs {
            font-size: 0.75rem;
        }

        .loadingText {
            font-size: 1rem;
        }
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
        <div class="bannerActions">
            <button class="homeBtn" on:click={() => goto("/")}>
                <img src={home} alt="Home" style="width: 24px; height: 24px;" />
            </button>
            <button class="uploadBtn" on:click={uploadFiles}>
                Upload Files
            </button>
        </div>
        <div class="introCard"> your stats   </div>
    </div>
   <div class= "details">
        {#if timeListened > 0}
            <div class="minutesCard">You've listened for {timeListened} minutes</div>
            <div class="songsCard">You've listened to {numberOfSongs} unique songs and {numberOfAlbums} unique albums</div>
        {:else}
            <!-- Placeholder state before upload -->
            <div class="minutesCard">Upload data to see stats</div>
            <div class="songsCard">Upload data to see stats</div>

        {/if}
    </div>

    <div class= "songs">
        <div class="songsListend">
            <h3>Top Songs</h3>
            {#if rankedSongs.length > 0}
                <ol class="songList">
                    {#each rankedSongs as [songName, ms]}
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
    made with love by <a href="https://github.com/CoolHackerMan27/" target="_blank" rel="noopener noreferrer">Plank</a>
    </div>
    
</div>