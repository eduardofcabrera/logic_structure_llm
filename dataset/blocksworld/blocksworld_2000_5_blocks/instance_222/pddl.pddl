

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(ontable c)
(on d a)
(ontable e)
(clear b)
(clear d)
)
(:goal
(and
(on a c)
(on c b)
(on d e))
)
)


