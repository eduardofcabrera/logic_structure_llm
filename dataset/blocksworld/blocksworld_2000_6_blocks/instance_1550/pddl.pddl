

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b a)
(on c b)
(ontable d)
(ontable e)
(clear c)
(clear d)
)
(:goal
(and
(on a c)
(on b a)
(on d e)
(on e b))
)
)


