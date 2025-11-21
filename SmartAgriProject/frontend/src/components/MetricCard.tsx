import { Card, CardContent } from '@/components/ui/card';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string;
  delta?: string | number;
  icon?: React.ReactNode;
}

export function MetricCard({ title, value, delta, icon }: MetricCardProps) {
  const deltaNum = typeof delta === 'string' ? parseFloat(delta) : delta;
  const isPositive = deltaNum !== undefined && deltaNum > 0;
  const isNegative = deltaNum !== undefined && deltaNum < 0;

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <p className="body-sm text-muted-foreground">{title}</p>
            <h3 className="heading-md mt-2">{value}</h3>
            {delta !== undefined && delta !== '' && (
              <div className={`flex items-center mt-2 body-sm ${isPositive ? 'text-success' : isNegative ? 'text-error' : 'text-muted-foreground'}`}>
                {isPositive && <TrendingUp size={16} className="mr-1" />}
                {isNegative && <TrendingDown size={16} className="mr-1" />}
                <span>{typeof delta === 'number' ? (delta > 0 ? `+${delta}` : delta) : delta}</span>
              </div>
            )}
          </div>
          {icon && <div className="text-primary-green">{icon}</div>}
        </div>
      </CardContent>
    </Card>
  );
}