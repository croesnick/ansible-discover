[![Build Status](https://travis-ci.org/croesnick/ansible-discover.svg?branch=master)](https://travis-ci.org/croesnick/ansible-discover)

# ansible-discover

_ansible-discover_ is a command line tool to list dependencies and dependants of [Ansible] roles and playbooks, respectively.

One of its prime uses is in a CI tool like Jenkins.
Once a change on, say a role, is committed, use _ansible-discover_ to gather the dependant roles and playbooks.
From this list, the respective CI jobs for playbook and role validations may then be triggered.

## Installation

```
pip3 install ansible-discover
```

## Usage

One use case (like outlined above) is to determine all roles (directly or indirectly) depending on a given set of roles: 
```
ansible-discover roles predecessors PATHS
```
where `PATHS` is a space-delimited list of paths to roles (e.g., `roles/my_sample_role`).

In addition to predecessors (i.e., dependants) for roles, you can also discover

* successors (i.e., dependencies) of roles: `ansible-discover roles successors`;
* predecessors for playbooks: `ansible-discover playbooks predecessors`; and
* successors of playbooks: `ansible-discover playbooks successors`.

## Related tools

- [ansigenome]
- [ansible-roles-graph]
- [ansible-review]

## License

Distributed under the XYZ license.
See `LICENSE.txt` for more information.

## Contributing

- Fork it!
- Create your feature branch: `git checkout -b my-new-feature`
- Commit your changes: `git commit -am 'Add some feature'`
- Push to the branch: `git push origin my-new-feature`
- Submit a pull request :)


[Ansible]: https://github.com/ansible/ansible
[ansigenome]: https://github.com/nickjj/ansigenome
[ansible-roles-graph]: https://github.com/sebn/ansible-roles-graph
[ansible-review]: https://github.com/willthames/ansible-review
