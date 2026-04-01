<script>
    import { resolve } from "$app/paths";
    import guy from '$lib/assets/image.png';

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
        min-height: 100vh;
        background-color: #f6ebc6;
        padding: 24px 16px;
        box-sizing: border-box;
    }

    .hero-image {
        width: min(70%, 720px);
        height: auto;
        margin-bottom: 40px;
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
        min-height: 48px;
        min-width: 220px;
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

    @media (max-width: 768px) {
        .hero-image {
            width: min(90%, 480px);
            margin-bottom: 28px;
        }

        .rickify-btn {
            width: min(100%, 340px);
            min-width: 0;
            font-size: 1.2rem;
            padding: 14px 22px;
        }
    }

    @media (max-width: 480px) {
        .container {
            padding: 20px 12px;
        }

        .hero-image {
            width: 100%;
            margin-bottom: 20px;
        }

        .rickify-btn {
            width: 100%;
            font-size: 1.05rem;
            padding: 12px 16px;
        }
    }
</style>

<div class="container">
    <img src={guy} alt="Rickify Logo" class="hero-image" />
    <button class="rickify-btn" on:click={navigate}>
        Rickify!
    </button>
</div>
