
### Introduction

[GitHub Actions](https://github.com/features/actions) makes it easy to automate all your software workflows with world-class CI/CD. Build, test, and deploy your code right from GitHub. [The C++ Alliance](https://cppalliance.org/) has been working on a project to translate pre-existing .travis.yml files into GitHub Actions format for Boost Libraries.  

### Instructions

There are different options to consider.  

1. If your .travis.yml has been kept reasonably up-to-date and/or contains customized tests, then the provided ci.yml is a convenient choice. It includes the same jobs as before. Merge the pull request which creates a .github/workflows/ci.yml file. Push another commit or pull request to trigger the CI tests. The same tests which passed on travis should be successful on GitHub Actions immediately.  

2. Another option, if your .travis.yml file is not current, could be to replace the entire workflow. In that case, do not merge the pull request. Copy a new template file from https://github.com/boostorg/boost-ci/blob/master/.github/workflows/ci.yml to your repository at .github/workflows/ci.yml. This may require debugging, it is not guaranteed to pass right away. The advantage of this choice is you will now have a relatively complete set of tests, if the previous .travis.yml file was not very extensive.  

3. Yet another option is a hybrid approach. Start with either of the files mentioned above. Copy-and-paste sections from the other file.  

If you have any questions or problems, please open an Issue in this github repo.  
