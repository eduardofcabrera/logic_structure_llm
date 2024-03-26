

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(ontable c)
(on d a)
(on e c)
(clear b)
)
(:goal
(and
(on a e)
(on c d)
(on d a))
)
)


