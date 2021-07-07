ansible_kube_bench
=========

An Ansible role to execute kube-bench

kube-bench is tool that checks whether Kubernetes is deployed securely by running the checks documented in the CIS Kubernetes Benchmark


https://www.cisecurity.org/benchmark/kubernetes/
https://github.com/aquasecurity/kube-bench


Build Status
----------------




Download last Version
----------------
https://github.com/aquasecurity/kube-bench/releases/latest


Manual Execution
----------------

  ansible-playbook -i inventory/inventory-test playbooks/ExecuteKubeBench.yml -e affected_host=all


License
-------

BSD


Author Information
------------------

Jan Souza
