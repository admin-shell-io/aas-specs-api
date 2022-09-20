# Contributing

The specification of [Asset Administration Shell - Part 2] is an official publication of the joint working group "Asset Administration Shell" of the [Platform Industrie 4.0] and [IDTA].
The specification and the API descriptions must be particularly compliant with this.
However, we highly invite the community to review, report and fix the definitions. 
To keep the management effort under control, we demand a defined procedure for the contribution in this repository.

[Asset Administration Shell - Part 2]: https://www.plattform-i40.de/PI40/Redaktion/EN/Standardartikel/specification-administrationshell.html

## Before the Pull Requests

**Create Feature branches**.
We develop using the feature branches, see [this section of the Git book].

[this section of the Git book]: https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows.

If you are a member of the development team, [create a feature branch] directly within the repository.

[create a feature branch]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository

Otherwise, if you are a non-member contributor, fork the repository and create the feature branch in your forked repository. See [this Github tutorial] for more guidance.
Please **do not** fork the SwaggerHub APIs and simply point to your updated API.
SwaggerHub does not provide any difference view, increasing the manual effort unnecessarily.

[this Github tutorial]: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork

**Branch Prefix**.
Please prefix the branch with your Github user name (*e.g.,* `sebbader/Add-some-feature`).

## Recommendation for Commit Messages

The commit messages follow the guidelines from https://chris.beams.io/posts/git-commit:
* Separate subject from body with a blank line
* Limit the subject line to 50 characters
* Capitalize the subject line
* Do not end the subject line with a period
* Use the imperative mood in the subject line
* Wrap the body at 72 characters
* Use the body to explain *what* and *why* (instead of *how*)


## Create Pull Request
After all changes have been committed to your feature branch, a [pull request] (PR) has to be created.
Every PR should be linked to an issue for tracking.
See [this Github tutorial] for more guidance. 

[pull request]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

[link PR to issue]: https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue


## Approval Process
All changes must be **reviewed** and **approved**.

Minor changes (simple failures, typos, *etc.*) and additional content (more examples, etc.) can be accepted straight away after a brief review by the responsible reviewers.

Major changes must first be reviewed and approved by the joint working group "Asset Administration Shell" of the [Platform Industrie 4.0] and [IDTA].

[Platform Industrie 4.0]: http://www.plattform-i40.de
[IDTA]: https://industrialdigitaltwin.org/



## Merge into Master Branch

After the approval the pull request can be merged into the repository. This is done by one of the maintainers.


## Post-Merge Cleanup
**Congratulation.**
You successfully contributed to the aas-spec repository.

If you are a member of the development team, please delete the feature branch you directly created within the aas-specs repository.

Otherwise, if you are not part of the team and you forked the repository, feel free to delete your fork.
