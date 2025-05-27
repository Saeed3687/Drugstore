/**
 * @jest-environment jsdom
 */

let currentRating;
let ratingDiv;
let allStars;

beforeEach(() => {
  document.body.innerHTML = `
    <div class="rating">
      <span class="star">☆</span>
      <span class="star">☆</span>
      <span class="star">☆</span>
      <span class="star">☆</span>
      <span class="star">☆</span>
      <input type="radio" name="rating" value="5" />
    </div>
  `;

  currentRating = 3;
  ratingDiv = document.querySelector(".rating");
  allStars = ratingDiv.querySelectorAll(".star");
});

function setStars(rating) {
  allStars.forEach((star, index) => {
    star.textContent = index < rating ? "★" : "☆";
  });
}

function highlightStars(star) {
  const index = [...allStars].indexOf(star);
  allStars.forEach((s, i) => {
    s.textContent = i <= index ? "★" : "☆";
  });
}

function resetStars() {
  setStars(currentRating);
}

function selectStar(star) {
  const input = star.parentNode.querySelector("input");
  input.checked = true;
  input.dispatchEvent(new Event("change"));
}

test("setStars displays the correct number of stars", () => {
  setStars(2);
  const filled = [...allStars].filter(s => s.textContent === "★");
  expect(filled.length).toBe(2);
});


test("highlightStars changes stars on hover", () => {
  highlightStars(allStars[4]);
  const filled = [...allStars].filter(s => s.textContent === "★");
  expect(filled.length).toBe(5);
});

test("resetStars restores current rating", () => {
  highlightStars(allStars[4]);
  resetStars();
  const filled = [...allStars].filter(s => s.textContent === "★");
  expect(filled.length).toBe(3);
});

