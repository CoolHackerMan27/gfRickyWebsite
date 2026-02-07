<script>
    import { resolve } from "$app/paths";
    import guy from '$lib/assets/image.png';

    let backColor  = '#f6ebc6'
    let forColor =  '#5276b4'

    function navigate(){
        window.location.href = resolve("/details")
    }
</script>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-color: #f6ebc6;
    }

    .rickify-btn {
        background-color: #5276b4;
        color: #f6ebc6;
        border: 3px solid #333;
        border-radius: 8px;
        padding: 16px 32px;
        font-size: 1.5rem;
        font-weight: bold;
        cursor: pointer;
        height: 12%;
        width: 25%;
        transition: all 0.2s ease;
        box-shadow: 4px 4px 0px #333;
    }

    .rickify-btn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #333;
    }

    .rickify-btn:active {
        transform: translate(4px, 4px);
        box-shadow: none;
    }
</style>

<div class="container">
    <img src={guy} alt="Rickify Logo" style="width: 70%; height: auto; margin-bottom: 40px;" />
    <button class="rickify-btn" on:click={navigate}>
        Rickify!
    </button>
</div>
