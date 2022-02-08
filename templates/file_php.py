registration = """<?php
{copyright}

declare(strict_types=1);

use Magento\\Framework\\Component\\ComponentRegistrar;

ComponentRegistrar::register(
	ComponentRegistrar::MODULE,
	'{module}',
	__DIR__
);
"""

controllerController = """<?php
{copyright}
namespace {vendor}\\{module}\\{namespace};

class {classs} extends \\Magento\\Framework\\App\\Action\\Action
{{
	protected $_pageFactory;

	public function __construct(
		\\Magento\\Framework\\App\\Action\\Context $context,
		\\Magento\\Framework\\View\\Result\\PageFactory $pageFactory)
	{{
		$this->_pageFactory = $pageFactory;
		return parent::__construct($context);
	}}

	public function execute()
	{{
		return $this->_pageFactory->create();
	}}
}}
"""

controllerBlock = """<?php
{copyright}
namespace {vendor}\\{module}\\{namespace};

class {classs} extends \\Magento\\Framework\\View\\Element\\Template
{{

}}
"""

controllerTemplate = """<?php
{copyright}

/** @var \\{vendor}\\{module}\\{block} $block */
?>
<h1><?php echo __('Welcome to %1', "{vendor}_{module} => {file}") ?></h1>
"""