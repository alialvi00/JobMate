

fetch('../../scrapers/jsonOutputs/glassdoor_jobs.json')
.then(response => response.json())
.then(data => {
  const jobListings = data.Jobs;
  jobListings.forEach(job => {
    const jobTitle = job["Job Title:"];
    const employerName = job["Employer name: "];
    const jobLocation = job["Job Location: "];
    const jobDetails = job["Job Details: "];
    const linkToJob = job["Link To Job: "];
    const jobListingElement = document.createElement("div");
    jobListingElement.classList.add("job-listing");
    jobListingElement.innerHTML = `
      <h2>${jobTitle}</h2>
      <p>${employerName}</p>
      <p>${jobLocation}</p>
      <div class="job-description-container">
        <div class="job-description">
          <p>${jobDetails}</p>
          <a href="${linkToJob}">View Job</a>
        </div>
      </div>
    `;
    const jobListContainer = document.getElementById("job-list-container");
    jobListContainer.appendChild(jobListingElement);
  });
});


